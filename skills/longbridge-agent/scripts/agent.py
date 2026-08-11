#!/usr/bin/env python3
"""Talk to a Longbridge AI agent without the longbridge CLI.

Fallback path only. When `longbridge` is installed, use it — it is faster,
better tested, and this file exists so a machine without it is not stuck.

Self-contained: standard library only, no `pip install`, no sibling modules.
Copy this one file anywhere and it runs.

Auth is the OAuth 2.0 device flow: no local callback server, so it works over
SSH and inside containers. The token is cached at ~/.longbridge/agent-token.json
with 0600 permissions and refreshed when it expires.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Access point. `.cn` and `.com` are CDN-style routes to the same data, not
# separate environments — a token from one is accepted by the other. They differ
# only in reach: `.com` can authorize accounts in both data centers, `.cn` only
# AP ones, while mainland-China networks may not reach `.com` at all. Defaulting
# to `.cn` keeps that network working; override for a US account.
API_HOST = os.environ.get("LONGBRIDGE_HTTP_URL", "https://openapi.longbridge.cn").rstrip("/")

# Global access point. The US data center is reachable ONLY through `.com` —
# `.cn` has no route to it and rejects US credentials outright no matter what
# `x-dc-region` says, because the header selects a data center, it cannot create
# a route to one.
API_HOST_GLOBAL = "https://openapi.longbridge.com"

# Where a human can open the same conversation in a browser — to see the
# charts and quote cards a terminal cannot render, or to keep chatting there.
# The trailing path segment is the chat_uid.
CONVERSATION_URL = "https://longbridge.com/ai/c/"

# Data center — orthogonal to the access point. A device_code is minted on AP
# and replicated to US, so the same code can be approved in either and we cannot
# know in advance which holds the account. Poll both, each at a host that can
# actually reach it.
DC_REGIONS = ("ap", "us")


def _host_for_region(region):
    return API_HOST_GLOBAL if region == "us" else API_HOST


def _region_of(credential):
    """Read the data center off a credential's `us_…` / `ap_…` prefix.

    The prefix is part of what the server stored, so it is authoritative — and
    it is the only way to know where a refresh token belongs.
    """
    return "us" if str(credential).startswith("us_") else "ap"


# Any id that reaches a request path must match this exactly. `fullmatch` plus
# no `$` anchor, because `$` would also accept one trailing newline.
ID_RE = re.compile(r"[A-Za-z0-9_-]{1,64}")

# Whether an unmatched value is worth retrying as a public agent's uid.
#
# This is the same grammar as ID_RE on purpose. Real uids are not all
# machine-generated: `chatbot` (LongbridgeAI) is public, reachable, and looks
# exactly like a word. Demanding a digit or a minimum length would reject the
# single most useful public agent to spare the user one clear failure on a
# typo'd name — a bad trade. Names with spaces or non-ASCII still fall out,
# which covers the common mistake.
UID_RE = ID_RE

# RFC 6750 bearer-token alphabet, plus the separators seen in practice.
CREDENTIAL_RE = re.compile(r"[A-Za-z0-9\-._~+/=]{1,4096}")
OAUTH_BASE = f"{API_HOST}/oauth2"
TOKEN_CACHE = pathlib.Path.home() / ".longbridge" / "agent-token.json"
# The CLI registers its own client; reuse that registration when present so a
# machine that once had the CLI does not have to authorize twice.
CLI_REGISTRATION = pathlib.Path.home() / ".longbridge" / "openapi" / "cli-registration"
# Questions an interrupted run asked, so `--continue` (a new process) can ask
# them back and key the answers correctly. The reference CLI keeps the same
# cache (ai_interrupts) for the same reason.
INTERRUPT_CACHE = pathlib.Path.home() / ".longbridge" / "agent-interrupts"

AGENT_PAGE_SIZE = 100  # server defaults to 20; larger pages mean fewer 429s
MAX_PAGES = 50
# Per-poll ceiling during device login. Must stay well under the ~300s window:
# a host that accepts the connection and never answers would otherwise consume
# the entire authorization period on its own.
POLL_TIMEOUT = 20
# How many transport failures before a data center is written off. One is
# too few: a single timed-out body would abandon a region that is merely
# slow, not unroutable.
MAX_REGION_FAILURES = 3
# Upper bound on any server-supplied lifetime, in seconds (~1 year). Beyond
# this the value is not a lifetime, it is a malformed field.
MAX_LIFETIME = 31_536_000
THROTTLE = 0.35  # seconds between listing calls — the API rejects bursts (429002)
# Longest credential we build a redaction pattern for. Ours are well under
# this; a longer one is covered by exact-form replacement alone.
MAX_PATTERN_SECRET = 512


# ---------------------------------------------------------------- http


# Fields whose values must never reach a terminal, a log, or a bug report.
# An error body can legitimately echo the credential that was sent, so the
# body cannot be displayed verbatim just because the request failed.
SECRET_FIELDS = ("access_token", "refresh_token", "device_code", "code",
                 "client_secret", "id_token", "authorization")


# Credential values this process has handled. Matching field names alone
# cannot catch an unlabelled echo — a server replying "refresh token us_… is
# invalid" defeats any field list — so the values themselves are registered
# and replaced exactly wherever they turn up.
_SENSITIVE_VALUES = set()

# One pattern per credential, matching it however it is encoded. See
# `_remember_secret`.
_SENSITIVE_PATTERNS = []


def _remember_secret(value):
    """Register a credential so it can never be echoed back to a terminal.

    Registers every decoded form, and a pattern that matches the credential
    under any percent-encoding. Exact forms alone were not enough: a server
    can echo `ap%255Fsecret` (two unquotes recover it), and `quote` leaves the
    RFC-unreserved characters alone, so `ap%5Fsecret` was never registered at
    all. The pattern lets each character appear raw or encoded, at any nesting
    depth — `%25` is itself an encoded `%`, so `%(?:25)*5F` covers `%5F`,
    `%255F`, and deeper.
    """
    if not isinstance(value, str) or len(value) < 8:
        return
    forms = _decodings(value)
    _SENSITIVE_VALUES.update(forms)
    if len(forms[-1]) > MAX_PATTERN_SECRET:
        # The pattern is ~35 bytes per character. A credential this long is
        # not one we minted, and compiling a pattern for it would cost more
        # than the exact forms above already cover.
        return
    _SENSITIVE_PATTERNS.append(re.compile("".join(
        f"(?:{re.escape(ch)}|%(?:25)*{_hex_branch(ch)})" if ord(ch) < 128
        else re.escape(ch)
        for ch in forms[-1])))


def _hex_branch(ch):
    """`5F` as `[5][Ff]` — the hex escape of `ch`, either case.

    Spelled out per digit rather than compiling the whole pattern with
    IGNORECASE, which would also have made the literal characters of the
    credential case-insensitive and over-redacted ordinary text.
    """
    return "".join(f"[{d}{d.lower()}]" if d.isalpha() else d
                   for d in f"{ord(ch):02X}")


def _decodings(value):
    """Every distinct form of `value`, down to its fully decoded fixed point.

    A true fixed point, not a layer count: bounding the search at two decodes
    let `ap%25255Fsecret` through, and a bound of eight simply moved the same
    hole to nine. This terminates on its own — decoding never lengthens a
    string, and a form that stops changing ends the loop — so the only limit
    is the input's own length.
    """
    forms, form = [], str(value or "")
    for _ in range(len(form) + 1):
        if not form or form in forms:
            break
        forms.append(form)
        # `unquote`, never `unquote_plus`: a credential may legally contain a
        # literal `+` (it is in CREDENTIAL_RE), and decoding `+` to a space
        # corrupted every derived form — the encoded echo of a token with a
        # `+` in it then matched nothing. A credential cannot contain a space,
        # so reading `+` as one can never be right here.
        decoded = urllib.parse.unquote(form)
        if decoded == form:
            break
        form = decoded
    return forms


def _hides_secret(text, secret):
    """Whether `text` contains `secret` under any layer of URL encoding."""
    return any(secret in form for form in _decodings(text))


# Terminal control characters, minus tab and newline. Semantic text we
# deliberately display — an agent's answer, a workspace name — is not a
# credential risk but is still attacker-influenced, and a raw escape sequence
# in it drives the terminal (an OSC-52 payload rewrites the clipboard).
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]")


def _display(text):
    """A string safe to put in front of a human.

    Both halves are needed. Stripping controls stops an answer from driving
    the terminal; replacing known credentials stops one from being read off
    it. An agent's answer is semantic content we mean to display, but it is
    still text somebody else wrote, and nothing prevents it from quoting a
    token this process is holding.
    """
    return _CONTROL_RE.sub("", _redact_known(str(text)))


def _clean(value, depth=0):
    """`_display` applied to every string inside a structure.

    For `--json`. The same rule as the rendered report, so the two outputs
    can never disagree about what is safe to show — and `json.dumps` alone
    does not help: with `ensure_ascii=False` it passes C1 controls through
    literally, and it never redacts anything.
    """
    if depth > 64:
        # Deeper than anything this API returns. Recursing into a maliciously
        # nested payload ends in a RecursionError traceback — an exit that
        # bypasses the gate — so it is cut off with a placeholder instead.
        return "<nesting too deep>"
    if isinstance(value, str):
        return _display(value)
    if isinstance(value, dict):
        # Keys as well as values: server-controlled event names become the
        # keys of `events`, and a key is printed exactly like a value is.
        return {(_display(k) if isinstance(k, str) else k): _clean(v, depth + 1)
                for k, v in value.items()}
    if isinstance(value, list):
        return [_clean(v, depth + 1) for v in value]
    return value


# Characters a credential can consist of — raw, or percent-encoded at any
# depth. CREDENTIAL_RE and the encoded alphabet (`%` plus hex digits) both
# stay inside this set, which is what makes the streaming hold-back below
# sound: no credential can span a character outside it.
_SECRET_RUN = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~+/=%")

# Longest unbroken run the live echo will hold before deciding the text is
# not prose and withholding it from the echo altogether. The final rendered
# answer is unaffected — it always arrives complete and sanitised.
MAX_ECHO_RUN = 16384


class _Echo:
    """Live echo of the answer that can never split a credential.

    `emit` inspects one write at a time, so a credential split across two SSE
    events used to stream out as two clean-looking halves, contiguous on the
    terminal. A credential is a single unbroken run of `_SECRET_RUN`
    characters, so the echo holds the trailing run back until a character
    outside the set closes it, then sanitises the run in one piece. Prose is
    unaffected — spaces, newlines and CJK all end the run — so at most one
    word ever lags. A run past `MAX_ECHO_RUN` is not prose: it is withheld
    entirely rather than cut at a point a credential could straddle.
    """

    def __init__(self, file):
        self.file = file
        self.held = ""
        self.muted = False  # inside an over-long run: drop text until it ends

    def write(self, text):
        buf = self.held + str(text)
        self.held = ""
        if self.muted:
            for i, ch in enumerate(buf):
                if ch not in _SECRET_RUN:
                    self.muted = False
                    buf = buf[i:]
                    break
            else:
                return
        cut = len(buf)
        while cut and buf[cut - 1] in _SECRET_RUN:
            cut -= 1
        if len(buf) - cut > MAX_ECHO_RUN:
            self.muted = True
        else:
            self.held = buf[cut:]
        if cut:
            emit(buf[:cut], file=self.file, end="")

    def close(self):
        # End of stream: nothing can extend the run, so it is safe to show.
        if self.held and not self.muted:
            emit(self.held, file=self.file, end="")
        self.held, self.muted = "", False


def emit(text="", *, file=None, end="\n"):
    """The single gate for human-facing output.

    Every `print` in this script goes through here, and `--json` goes through
    `_clean`, so the rules live in one place instead of at each call site.
    """
    stream = file or sys.stdout
    stream.write(_display(text) + end)
    stream.flush()


# The OAuth error codes we act on or report. A closed vocabulary, because a
# character grammar accepted a credential as an "error code" and printed it.
OAUTH_ERROR_CODES = frozenset({
    "invalid_request", "invalid_client", "invalid_grant", "invalid_scope",
    "unauthorized_client", "unsupported_grant_type", "unsupported_response_type",
    "access_denied", "server_error", "temporarily_unavailable",
    "authorization_pending", "slow_down", "expired_token", "invalid_token",
})


def _is_oauth(url):
    """Whether a URL belongs to the credential-bearing OAuth endpoints."""
    return "/oauth2/" in str(url)


def _oauth_detail(body):
    """The OAuth error code, and nothing else.

    `error_description` is free text the server controls, and it does carry
    credentials — a probe found a device code echoed there percent-encoded,
    which no redaction of registered values can match. The spec-defined
    `error` code is a closed vocabulary and is enough to act on; the rest of
    the body never reaches a human.
    """
    try:
        payload = json.loads(body)
    # ValueError rather than JSONDecodeError: CPython also refuses to build an
    # int from a literal over 4,300 digits, raising a bare ValueError for it.
    except (ValueError, TypeError):
        payload = None
    if not isinstance(payload, dict):
        return "unreadable error body (not shown)"
    code = payload.get("error")
    if isinstance(code, str) and code in OAUTH_ERROR_CODES:
        return code
    return "unspecified error (body not shown)"


def _api_detail(body):
    """A safe summary of an ordinary API error body.

    The numeric `code` this API uses (429002 for rate limiting, say) is a
    number, so it cannot carry a credential — and it is the field worth
    reporting. Routing these through the OAuth formatter turned every
    documented error code into "unspecified".
    """
    try:
        payload = json.loads(body)
    except (ValueError, TypeError):   # including an over-long int literal
        payload = None
    if not isinstance(payload, dict):
        return "unreadable error body (not shown)"
    code = payload.get("code")
    # Bounded, not just numeric: on Python 3.9 a 5,000-digit literal parses
    # fine, and formatting it would put 5,000 characters on the terminal.
    # Real codes are six digits.
    if isinstance(code, int) and not isinstance(code, bool) and abs(code) < 10 ** 12:
        return f"code={code} (body not shown)"
    return "unspecified error (body not shown)"


def _redact_known(text):
    """Remove credentials this process is holding, and nothing else.

    Two layers: exact replacement catches an unlabelled echo, which no field
    list can, and a per-credential pattern catches the same value
    percent-encoded, which exact replacement cannot enumerate.

    Safe to apply to an agent's answer, because it only ever matches a real
    credential. `_redact` below adds guesswork on top and is not.
    """
    if not text:
        return text
    out = str(text)
    for secret in _SENSITIVE_VALUES:
        out = out.replace(secret, "<redacted>")
    for pattern in _SENSITIVE_PATTERNS:
        out = pattern.sub("<redacted>", out)
    return out


def _redact(text):
    """`_redact_known`, plus a guess at secrets we have never seen.

    The field patterns matter for a credential minted by the server inside a
    body we then failed to parse — but they are heuristics, and would rewrite
    an answer that merely says `code=42`. So this is for raw bodies only;
    displayed prose gets `_redact_known`.
    """
    if not text:
        return text
    out = _redact_known(text)
    for field in SECRET_FIELDS:
        # "field":"value" / 'field':'value' / field=value, tolerating a
        # truncated body whose closing quote never arrived.
        out = re.sub(rf'(["\']{field}["\']\s*:\s*["\'])[^"\']*(["\']|$)',
                     r"\1<redacted>\2", out, flags=re.IGNORECASE)
        out = re.sub(rf"(\b{field}=)[^&\s\"']+", r"\1<redacted>", out, flags=re.IGNORECASE)
    # `Authorization: Bearer <token>` from an echoed request dump.
    out = re.sub(r"(bearer\s+)\S+", r"\1<redacted>", out, flags=re.IGNORECASE)
    return out


class ApiError(Exception):
    """An HTTP error with its status and parsed body kept separate.

    Callers classify on `payload["error"]` rather than on rendered text —
    matching substrings of a message is fragile once a server puts an OAuth
    error name inside a human-readable description.
    """

    def __init__(self, status, url, body, authenticated=False):
        # A body from a credential-bearing request is never shown. Redaction
        # cannot be made
        # airtight against a body we do not control — a token can be echoed
        # URL-encoded, split across lines, or minted by the server and never
        # registered. Structured fields are safe; the raw text is not.
        if authenticated or _is_oauth(url):
            detail = (_oauth_detail(body) if _is_oauth(url)
                      else _api_detail(body))
            super().__init__(f"HTTP {status} {url}: {detail}")
        else:
            super().__init__(f"HTTP {status} {url}\n{_redact(body)[:800]}")
        self.status = status
        self.body = body
        try:
            decoded = json.loads(body)
        except (ValueError, TypeError):   # including an over-long int literal
            decoded = None
        # An error body may legally be a list or a string; only an object
        # has fields to classify on.
        self.payload = decoded if isinstance(decoded, dict) else {}

    @property
    def oauth_error(self):
        # Only a string: `"error": ["invalid_grant"]` used to reach a set
        # membership test and raise TypeError.
        code = self.payload.get("error")
        return code if isinstance(code, str) else ""


class ProtocolError(Exception):
    """The server answered, but not with something we can read fields off.

    Distinct from ApiError because there is no HTTP error to report: reusing
    `ApiError(200, …)` for this told the user "HTTP 200" about a failure.
    """

    def __init__(self, url, detail, body="", status=None, authenticated=False):
        where = f"HTTP {status} " if status is not None else ""
        # Same rule as ApiError: any credential-bearing exchange may echo a
        # server-minted secret we never registered, so its body is hidden.
        shown = "" if (authenticated or _is_oauth(url)) else _redact(str(body))[:400]
        super().__init__(f"{where}{url}: {detail}\n{shown}".rstrip())
        self.url = url
        self.detail = detail
        self.body = body
        self.status = status


class TransportError(Exception):
    """The exchange broke: no response, or one that could not be read.

    Kept separate from `ApiError` so a caller can tell "this data center is
    unreachable from here" (routine: `.com` is often blocked from mainland
    China) from "the server rejected this request". It also covers a body
    that fails midway after headers arrived, which is why the message does
    not claim nothing was received.
    """

    def __init__(self, url, reason):
        self.reason = _safe_reason(reason)
        super().__init__(f"Network exchange with {url} failed: {self.reason}")
        self.url = url


def _safe_reason(exc):
    """Why an exchange failed, in words that cannot come from the server.

    `str(exc)` looked harmless and was not: `http.client` builds its message
    out of the bytes it choked on, so a reply whose status line is a bearer
    token reproduces that token verbatim. Nothing here is server-derived —
    `strerror` is the C library's text for an errno, and the fallback is a
    class name.
    """
    if isinstance(exc, urllib.error.URLError) and isinstance(exc.reason, BaseException):
        exc = exc.reason
    if isinstance(exc, TimeoutError):
        return "timed out"
    if isinstance(exc, http.client.HTTPException):
        # Deliberately not `str(exc)`: this is the class whose messages quote
        # the response bytes.
        return f"malformed HTTP response ({type(exc).__name__})"
    if isinstance(exc, OSError) and exc.strerror:
        return exc.strerror
    return type(exc).__name__


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse redirects outright.

    urllib replays the Authorization header onto a cross-origin redirect, so
    one 302 from the configured host is enough to hand a bearer token to
    somebody else. No Longbridge API endpoint redirects, so failing is safe.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # urllib closes `fp` only after this returns, and we never return —
        # close it here or the socket stays open.
        try:
            fp.close()
        except Exception:  # noqa: BLE001 — closing must not mask the refusal
            pass
        # The Location header is server-controlled and can carry a
        # percent-encoded bearer token. The redirect is refused either way,
        # so the target adds nothing worth the risk of printing it.
        authed = any(k.lower() == "authorization" for k in (req.headers or {}))
        raise ApiError(code, req.full_url,
                       '{"error":"unexpected_redirect"}', authenticated=authed)


_OPENER = urllib.request.build_opener(_NoRedirect)


def _seg(value):
    """Validate, then percent-encode, one path segment.

    Encoding alone is not enough: `.` is RFC-unreserved, so `quote("..")` is
    `".."` — a real parent segment that survives into the request path and
    invites proxy-side normalization. Ids are opaque identifiers, so require
    the identifier grammar first and reject anything else outright.
    """
    text = str(value)
    if not ID_RE.fullmatch(text):
        raise SystemExit(
            f"Refusing {text!r} as a path segment: ids must match {ID_RE.pattern} "
            "(this rejects '.', '..', slashes and control characters)."
        )
    return urllib.parse.quote(text, safe="")


def _check_origin(url):
    """Only https, and only to an access point we know."""
    allowed = {API_HOST, API_HOST_GLOBAL}
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https":
        raise SystemExit(f"Refusing a non-HTTPS request to {url!r} — a bearer token would "
                         "cross the network in the clear.")
    if f"{parts.scheme}://{parts.netloc}" not in allowed:
        raise SystemExit(f"Refusing to send credentials to {parts.netloc!r}; expected one of "
                         + ", ".join(sorted(allowed)))


# Everything that means "the exchange broke" rather than "the server
# answered". http.client.HTTPException is in here because IncompleteRead —
# a truncated body — is not an OSError and would otherwise escape raw.
TRANSPORT_ERRORS = (urllib.error.URLError, OSError, http.client.HTTPException)


def _drain(resp, url):
    """Read a response to the end and close it, whatever happens.

    Every response — success or HTTPError — goes through here, so there is one
    place that owns closing and one place that turns a broken read into a
    TransportError. Earlier versions had this logic duplicated per call site
    and each copy missed a different case.
    """
    try:
        return resp.read().decode("utf-8", "replace")
    except TRANSPORT_ERRORS as exc:
        raise TransportError(url, exc) from None
    finally:
        try:
            resp.close()
        except Exception:  # noqa: BLE001 — a close failure must not mask the read result
            pass


def _decode_object(raw, url, status=200, authenticated=False):
    """Decode a JSON *object*, or fail with ProtocolError.

    An endpoint answering with `[]`, `"text"`, `null` or non-JSON is not
    something later code can read fields off. Rejecting it once, here, keeps
    every caller from having to guard `.get()`.
    """
    if not raw.strip():
        if not _is_oauth(url):
            # An ordinary endpoint always answers with an envelope. Returning
            # {} here skipped the envelope check entirely, and every caller
            # then read the empty result as "you have none of these".
            raise ProtocolError(url, "empty response body", raw, status,
                                authenticated=authenticated)
        return {}
    try:
        value = json.loads(raw)
    except ValueError:
        # Not only malformed JSON: CPython refuses to build an int from a
        # literal over 4,300 digits, and raises a bare ValueError for it.
        raise ProtocolError(url, "response is not JSON", raw, status,
                            authenticated=authenticated) from None
    if not isinstance(value, dict):
        raise ProtocolError(url, f"expected a JSON object, got {type(value).__name__}",
                            raw, status, authenticated=authenticated) from None
    if _is_oauth(url):
        # OAuth replies are flat by spec — there is no envelope to open.
        return value
    return _unwrap(value, raw, url, status, authenticated)


def _unwrap(envelope, raw, url, status, authenticated):
    """The `data` payload of a Longbridge API envelope.

    Every non-OAuth endpoint answers `{"code":0,"message":"success","data":{…}}`.
    Reading fields off the envelope instead of `data` is not a parse error —
    `.get("workspaces")` simply returns None — so it surfaced as "this account
    belongs to no workspace" for every account, which is why it survived
    review. Opening the envelope here, once, is what keeps a shape change from
    failing quietly again.
    """
    code = envelope.get("code")
    if code is not None and (isinstance(code, bool) or not isinstance(code, int)):
        # `"code": "429002"` is not something we can compare against 0, and
        # ignoring it let a failed call through as a success.
        raise ProtocolError(url, f"envelope `code` is {type(code).__name__}, not an integer",
                            raw, status, authenticated=authenticated)
    if isinstance(code, int) and code != 0:
        # A business error carried by a 200. It is an API failure, not a
        # malformed response, so callers can classify it as one.
        raise ApiError(status, url, raw, authenticated=authenticated)
    if "data" not in envelope:
        if "code" not in envelope:
            raise ProtocolError(url, "response is not a Longbridge API envelope",
                                raw, status, authenticated=authenticated)
        # A call that reports success and returns nothing.
        return {}
    data = envelope["data"]
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ProtocolError(url, f"expected an object under `data`, got {type(data).__name__}",
                            raw, status, authenticated=authenticated)
    return data


def _request(method, url, *, headers=None, data=None, stream=False, timeout=300):
    _check_origin(url)
    # Whether this exchange carried a credential decides whether its error
    # body may be shown. Ordinary API calls send a bearer token too, so the
    # rule cannot key on the URL alone.
    authed = any(k.lower() == "authorization" for k in (headers or {}))
    req = urllib.request.Request(url, method=method, data=data, headers=headers or {})
    try:
        resp = _OPENER.open(req, timeout=timeout)
    except urllib.error.HTTPError as exc:
        # If reading the error body fails, that is a transport failure, not a
        # fatal API answer — let `_drain`'s TransportError propagate. Swallowing
        # it produced a blank ApiError, which the poll loop classified as FATAL
        # and stopped retrying a data center that was merely slow.
        raise ApiError(exc.code, url, _drain(exc, url), authenticated=authed) from None
    except TRANSPORT_ERRORS as exc:
        # A distinct type, because "this host is unreachable" is not the same
        # as "this request failed": the device-flow loop must be able to write
        # off one data center and keep polling the other.
        raise TransportError(url, exc) from None
    if stream:
        # A 200 that is not an event stream (an error page, a JSON envelope)
        # would otherwise yield no events and be rendered as an empty, silently
        # truncated answer. Say what actually arrived instead.
        kind = (resp.headers.get("content-type") or "").split(";")[0].strip().lower()
        if kind and kind != "text/event-stream":
            # The media type is server-controlled: a probe recovered a token
            # from `Content-Type: application/ap_abcdef123`.
            detail = ("unexpected content type" if authed
                      else f"expected an event stream, got {kind}")
            raise ProtocolError(url, detail, _drain(resp, url), 200,
                                authenticated=authed)
        return resp
    return _decode_object(_drain(resp, url), url, authenticated=authed)


def _form(url, fields, headers=None, timeout=300):
    body = urllib.parse.urlencode(fields).encode()
    head = {"content-type": "application/x-www-form-urlencoded"}
    head.update(headers or {})
    # Shape is enforced centrally by `_decode_object`.
    return _request("POST", url, headers=head, data=body, timeout=timeout)


# ---------------------------------------------------------------- auth


def _text(value):
    """A non-empty string, or None. For fields read as text."""
    return value if isinstance(value, str) and value else None


def _identifier(value):
    """An id safe to put in a request path, or None.

    Numeric workspace ids arrive as JSON numbers and string uids as strings,
    so both are accepted — but `str(None)` is `"None"`, which is a perfectly
    valid-looking path segment and 404s several calls later.
    """
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return str(value)
    text = _text(value)
    return text if text and ID_RE.fullmatch(text) else None


def _required(payload, field, url):
    """A field the endpoint is documented to return, or a ProtocolError.

    `.get(field)` returning None reads downstream as "you have none of
    these" — which is how a client reading the wrong nesting level reported
    "this account belongs to no workspace" to every account instead of
    failing.
    """
    if field not in payload:
        raise ProtocolError(url, f"response has no `{field}`")
    return payload[field]


def _credential(value):
    """A string usable as an HTTP header value, or None.

    A token containing CR/LF or surrounding whitespace passed the plain
    string check and then raised `ValueError: Invalid header value` deep
    inside http.client — a traceback instead of a diagnosis.
    """
    text = _text(value)
    if text is None or text != text.strip():
        return None
    # Must be encodable as a header: a token containing an emoji raised
    # UnicodeEncodeError inside http.client. The RFC bearer alphabet plus
    # the separators Longbridge uses is all that is allowed.
    return text if CREDENTIAL_RE.fullmatch(text) else None


def _finite(value):
    """A finite real number, or None.

    JSON `1e309` decodes to `inf`, which passed every numeric check and made a
    stale token look valid forever; a 401-digit integer passed too and then
    overflowed the arithmetic that used it.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    try:
        as_float = float(value)
    except (OverflowError, ValueError):
        return None
    return value if as_float == as_float and abs(as_float) != float("inf") else None


def _lifetime(value, default, url, field):
    """A positive whole number of seconds from an OAuth response.

    Absent means "use the default". Present but unusable does not: a lifetime
    of `"soon"`, `-1`, or `1e309` is a server contract violation, and silently
    substituting a default would hide it. `int()` alone was not enough — it
    accepts `True`, truncates `1.9`, and raises OverflowError on infinity.
    """
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ProtocolError(url, f"{field} is not a number")
    if isinstance(value, float):
        # 5.0 is integral and legal JSON; 5.5 is not a whole number.
        if _finite(value) is None or not value.is_integer():
            raise ProtocolError(url, f"{field} is not a whole number")
        seconds = int(value)
    else:
        try:
            seconds = int(str(value).strip())
        except (TypeError, ValueError, OverflowError):
            raise ProtocolError(url, f"{field} is not a whole number") from None
    if seconds <= 0:
        raise ProtocolError(url, f"{field} must be positive")
    # A 401-digit integer is a valid JSON number and passes every check
    # above, then overflows the arithmetic that adds it to a clock.
    if _finite(seconds) is None or seconds > MAX_LIFETIME:
        raise ProtocolError(url, f"{field} is implausibly large")
    return seconds


def _objects(value):
    """Keep only the dict members of a list. Returns (kept, rejected_count).

    Guarding the container but not its members left `references=["bad"]` to
    crash in the renderer — the collection was a list, so it passed, and each
    entry was then treated as a mapping.
    """
    if value is None:
        return [], 0          # absent: nothing was promised
    if not isinstance(value, list):
        return [], 1          # present but unusable: that is a defect
    kept = [v for v in value if isinstance(v, dict)]
    return kept, len(value) - len(kept)


def _read_json(path):
    """Read a cached JSON *object*, or None if it is unusable.

    Absent, corrupt, wrongly-encoded and non-object contents all mean the
    same thing to callers: there is nothing here to trust. Only a
    permission failure is worth interrupting for.
    """
    try:
        value = json.loads(path.read_text())
    except FileNotFoundError:
        return None
    except ValueError:   # JSONDecodeError and UnicodeDecodeError both derive from it
        return None  # corrupt cache — treat as absent and re-authorize
    except OSError as exc:
        # "I am not allowed to read it" is not "it is not there". Silently
        # re-authorizing here would loop the user through the browser flow on
        # every run without ever saying why.
        raise SystemExit(
            f"Cannot read {path} ({exc.strerror}). Fix its permissions or delete it."
        ) from None
    return value if isinstance(value, dict) else None


def _write_secret(path, payload):
    """Write a token file that is never briefly world-readable.

    Writing first and chmod-ing after leaves a window in which the secret is
    on disk under the process umask — 0644 on a stock machine. Open with the
    mode up front, and fchmod as well so an existing loose file is tightened
    before the new token goes into it.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as fh:
            os.fchmod(fh.fileno(), 0o600)
            json.dump(payload, fh, indent=2)
    except OSError as exc:
        # A read-only filesystem must not end a successful refresh with a
        # traceback; say what failed and that the session still works.
        raise SystemExit(
            f"Obtained a token but could not save it to {path} ({exc.strerror}). "
            "Fix the path or set HOME somewhere writable; this run cannot cache it."
        ) from None


def _client_id(explicit=None):
    if explicit:
        return explicit
    if env := os.environ.get("LONGBRIDGE_CLIENT_ID"):
        return env
    if reg := _read_json(CLI_REGISTRATION):
        if cid := reg.get("client_id"):
            return cid
    raise SystemExit(
        "No client_id. Pass --client-id, set LONGBRIDGE_CLIENT_ID, or install the\n"
        "longbridge CLI and run `longbridge auth login` once to create one."
    )


def _poll_region(region, client_id, device_code, timeout):
    """Poll one data center once. Returns (outcome, payload).

    Outcomes: TOKEN (payload is the token), WAIT, SLOW_DOWN, NOT_HERE
    (this DC has no such code), FATAL (payload is the error), TRANSPORT
    (payload is the reason). One classification in one place, so the caller
    never has to infer intent from which flag happens to be set.
    """
    # US is only routable via `.com`; the header alone cannot get us there
    # from `.cn`.
    url = f"{_host_for_region(region)}/oauth2/token"
    try:
        got = _form(
            url,
            {
                "client_id": client_id,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
            },
            headers={"x-dc-region": region},
            # Cap per request, never the whole remaining window: a blackholed
            # host would otherwise starve the region that can answer.
            timeout=timeout,
        )
    except TransportError as exc:
        return "TRANSPORT", exc.reason
    except ProtocolError as exc:
        # A garbled answer is still an answer — the host is reachable, so this
        # is not a transport failure, but it tells us nothing to act on.
        return "FATAL", exc
    except ApiError as exc:
        # Classify on the OAuth error field, not on rendered text: a
        # description mentioning "slow_down" must not be mistaken for one.
        if exc.oauth_error == "authorization_pending":
            return "WAIT", None
        if exc.oauth_error == "slow_down":
            return "SLOW_DOWN", None
        if exc.oauth_error == "invalid_grant":
            return "NOT_HERE", None
        return "FATAL", exc
    if got.get("access_token") is not None:
        return "TOKEN", got   # validated centrally by _ingest_token
    return "WAIT", None  # 200 without a token: still in progress


def _device_login(client_id):
    """OAuth device flow: show a code, poll until the user authorizes it."""
    url = f"{OAUTH_BASE}/device/authorize"
    start = _form(url, {"client_id": client_id})

    # Validate before printing anything. Without this, a response missing
    # `device_code` showed the user an authorization prompt, slept, and only
    # then died on a KeyError — after they had already opened the browser.
    device_code = _text(start.get("device_code"))
    uri = _text(start.get("verification_uri_complete")) or _text(start.get("verification_uri"))
    if not device_code:
        raise ProtocolError(url, "device authorization response has no device_code")
    if not _text(uri):
        raise ProtocolError(url, "device authorization response has no verification URI")
    _remember_secret(device_code)
    user_code = _text(start.get("user_code"))
    if not user_code and "user_code=" not in uri:
        raise ProtocolError(url, "device authorization response has no user_code")
    # The complete URI legitimately carries user_code; it must never carry
    # the device_code, which is the actual credential.
    # Both fields are printed to the terminal, so neither may hide the
    # device code under any layer of percent encoding — a single unquote
    # was not enough for `ap%255Fsecret`.
    if _hides_secret(uri, device_code):
        raise ProtocolError(url, "verification URI contains the device_code")
    if user_code and _hides_secret(user_code, device_code):
        raise ProtocolError(url, "user_code contains the device_code")
    interval = max(_lifetime(start.get("interval"), 5, url, "interval"), 1)
    # monotonic: a wall-clock adjustment mid-flow must not extend or cut the
    # window the server gave us.
    deadline = time.monotonic() + _lifetime(start.get("expires_in"), 300, url, "expires_in")

    emit(f"\nAuthorize this device:\n  {uri}"
         + (f"\n  code: {user_code}" if user_code else "") + "\n",
         file=sys.stderr)
    unreachable = set()   # data centers written off after repeated failures
    failures = {}         # consecutive transport failures per region
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        time.sleep(min(interval, remaining))
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break  # slept up to the deadline; a poll now would outlive the code

        # Poll each data center and classify the answer explicitly. Deriving
        # "keep waiting?" from a set of coupled flags is what previously let a
        # sub-threshold transport failure end the whole login: each outcome now
        # says for itself whether the region is still in play.
        waitable = False   # some region may still authorize
        fatal = None       # a real error, reported only if nothing is waitable
        for region in DC_REGIONS:
            if region in unreachable:
                continue  # written off earlier; do not pay for it every round
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                waitable = True  # out of time, not out of hope — let the outer
                break            # loop hit the deadline and report expiry

            outcome, payload = _poll_region(region, client_id, start["device_code"],
                                            min(POLL_TIMEOUT, remaining))

            if outcome == "TOKEN":
                return payload
            if outcome == "TRANSPORT":
                # Count consecutive failures only. A region that answers at all
                # is alive, so its count is cleared below — otherwise an
                # intermittent host is written off after three failures spread
                # across an entire successful session.
                failures[region] = failures.get(region, 0) + 1
                if failures[region] >= MAX_REGION_FAILURES:
                    unreachable.add(region)
                    emit(f"[warn] {region.upper()} data center unreachable after "
                         f"{failures[region]} attempts ({payload}); continuing with "
                         "the other one.", file=sys.stderr)
                else:
                    # Below the threshold this region is still a candidate, so
                    # the round must not be treated as hopeless.
                    waitable = True
                continue

            # Any HTTP answer proves the region is reachable.
            failures.pop(region, None)
            if outcome == "WAIT":
                waitable = True
            elif outcome == "SLOW_DOWN":
                interval += 5  # RFC 8628 §3.5 — back off on every poller
                waitable = True
            elif outcome == "NOT_HERE":
                pass  # this DC does not hold the code; the other one may
            else:  # FATAL
                fatal = fatal or payload

        if len(unreachable) == len(DC_REGIONS):
            raise SystemExit(
                "No Longbridge data center is reachable from this network — check "
                "connectivity, then run again."
            )
        if not waitable:
            # Every reachable region answered, none left room to wait.
            raise SystemExit(str(fatal) if fatal else
                             "Device code was not accepted by any data center — run again.")
    raise SystemExit("Device authorization expired before it was approved — run again.")


def _refresh(client_id, refresh_token):
    # The refresh token carries the data center it belongs to as a prefix, and
    # a US token can only be refreshed at `.com`. Send the prefix verbatim —
    # it is part of the credential the server stored.
    region = _region_of(refresh_token)
    return _form(
        f"{_host_for_region(region)}/oauth2/token",
        {
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        headers={"x-dc-region": region},
    )


# OAuth errors that mean the credential itself is dead. Anything else — a 503,
# throttling, a bad client_id — is the server's problem, not a reason to make
# the user authorize again.
_DEAD_CREDENTIAL = {"invalid_grant", "invalid_token", "expired_token"}


def _ingest_token(token, previous_refresh=None):
    """Validate, register, complete and cache a token payload. Returns the
    access token.

    Every credential this process accepts passes through here, whichever
    source produced it. Splitting that across the device, refresh and cache
    paths is what let a refresh response be cached without validation.
    """
    access = _credential(token.get("access_token"))
    if not access:
        raise ProtocolError(OAUTH_BASE, "token response has no usable access_token")
    refresh = token.get("refresh_token")
    if refresh is not None and not _credential(refresh):
        raise ProtocolError(OAUTH_BASE, "token response has an unusable refresh_token")
    # A refresh response may legally omit refresh_token, meaning "keep using
    # the one you have". Overwriting the cache with the response alone would
    # drop it and force a full device login at the next expiry.
    if not refresh and previous_refresh:
        token["refresh_token"] = previous_refresh
    _remember_secret(access)
    _remember_secret(_credential(token.get("refresh_token")))

    token["expires_at"] = time.time() + _lifetime(
        token.get("expires_in"), 3600, OAUTH_BASE, "expires_in")
    _write_secret(TOKEN_CACHE, token)
    return access


def access_token(client_id, force_login=False):
    cached = None if force_login else _read_json(TOKEN_CACHE)
    if cached:
        # Tighten the moment the file is read, before its refresh token is put
        # on the wire — not only on the still-valid path. A cache left loose by
        # an older version or a stray umask was otherwise used as-is and
        # hardened only after a new token had been written.
        try:
            if TOKEN_CACHE.stat().st_mode & 0o077:
                TOKEN_CACHE.chmod(0o600)
        except FileNotFoundError:
            cached = None  # vanished between read and stat; just re-authorize
        except OSError as exc:
            # The 0600 guarantee is the reason this file is safe to keep. If it
            # cannot be enforced, stop rather than put a refresh token on the
            # wire out of a cache anyone can read.
            raise SystemExit(
                f"Cannot secure {TOKEN_CACHE} ({exc.strerror}). Fix its permissions "
                "or delete it, then run again."
            ) from None

    # A cache field can be any JSON type. `expires_at` of "tomorrow" used to
    # raise TypeError on the comparison; anything unusable simply counts as
    # expired, and an unusable token counts as absent.
    expires_at = _finite(cached.get("expires_at")) if cached else None
    access = _credential(cached.get("access_token")) if cached else None
    refresh = _credential(cached.get("refresh_token")) if cached else None
    # Register before use, not only on the paths that mint a token: a cached
    # credential echoed back by an OAuth error was otherwise printed verbatim.
    _remember_secret(access)
    _remember_secret(refresh)

    if expires_at is not None and access and expires_at > time.time() + 60:
        return access

    token = None
    if refresh:
        try:
            token = _refresh(client_id, refresh)
        except ApiError as exc:
            if exc.oauth_error not in _DEAD_CREDENTIAL:
                # Surface it. Silently starting a device login here would ask
                # the user to re-authorize because a server returned 503.
                raise
            token = None  # genuinely revoked or expired — re-authorize
        else:
            # A refresh that answers 200 without a token is a broken response,
            # not a dead credential. Falling through would ask the user to
            # re-authorize in a browser because a server had a bad minute.
            if not _credential(token.get("access_token")):
                raise ProtocolError(f"{_host_for_region(_region_of(refresh))}/oauth2/token",
                                    "refresh succeeded but returned no usable access token")
    if not token or not token.get("access_token"):
        token = _device_login(client_id)

    # One ingestion point for every source — device flow, refresh, and the
    # carried-forward cache. Each of these used to validate (or not) on its
    # own, so a refresh response was cached without ever being checked.
    return _ingest_token(token, previous_refresh=refresh)


# ---------------------------------------------------------------- api


class Api:
    def __init__(self, token):
        self._auth = {"authorization": f"Bearer {token}"}
        # The access token carries its data center as a prefix, and `.cn` has
        # no route to US. Pick the host the token can actually be used at,
        # exactly as the refresh call does.
        self._host = _host_for_region(_region_of(token))

    def get(self, path, params=None):
        url = f"{self._host}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return _request("GET", url, headers=self._auth)

    def post_sse(self, path, body):
        return _request(
            "POST",
            f"{self._host}{path}",
            headers={**self._auth, "accept": "text/event-stream",
                     "content-type": "application/json"},
            data=json.dumps(body).encode(),
            stream=True,
        )


def iter_agents(api, workspace=None, partial=False):
    """Yield (workspace, agent) across every workspace, following pagination.

    Without paging, a workspace with many agents only ever shows its first 20 —
    which silently breaks name lookup and the ambiguity check below.
    """
    # Members matter, not just the container: a string workspace entry
    # passed the list check and then broke on `.get`.
    spaces, bad = _objects(_required(api.get("/v1/ai/workspaces"), "workspaces",
                                    f"{API_HOST}/v1/ai/workspaces"))
    if bad:
        # Dropping a member silently during discovery could hide the agent
        # that made a name ambiguous, turning a prompt into a wrong pick.
        raise ProtocolError(f"{API_HOST}/v1/ai/workspaces",
                            f"{bad} unusable workspace entries")
    if not spaces:
        raise SystemExit("This account belongs to no workspace.")
    for space in spaces:
        # A workspace without an id used to become the path segment "None"
        # and 404 further down. A missing name only costs a nicer label.
        sid = _identifier(space.get("id"))
        if sid is None:
            raise ProtocolError(f"{API_HOST}/v1/ai/workspaces",
                                "a workspace has no usable id")
        name = _text(space.get("name")) or ""
        if workspace and workspace.lower() not in (name.lower(), sid):
            continue
        page, seen = 1, 0
        while page <= MAX_PAGES:
            time.sleep(THROTTLE)
            data = api.get(f"/v1/ai/workspaces/{_seg(sid)}/agents",
                           {"page": page, "limit": AGENT_PAGE_SIZE})
            where = f"{API_HOST}/v1/ai/workspaces/{sid}/agents"
            agents, bad = _objects(_required(data, "agents", where))
            if bad:
                raise ProtocolError(where, f"{bad} unusable agent entries")
            # A string `total` used to raise TypeError on the comparison.
            total = _finite(data.get("total"))
            if total is not None and (total < 0 or total != int(total)):
                total = None
            if not agents:
                if total is not None and seen < total:
                    # The listing is provably incomplete. `--list` may show
                    # what arrived (with a warning), but resolving a *name*
                    # against a partial listing can silently pick the wrong
                    # agent: the one that would have made the name ambiguous
                    # may be exactly the one missing — and these agents can
                    # place real orders.
                    if not partial:
                        raise ProtocolError(
                            where, f"listing stopped at {seen} of {int(total)} agents; "
                            "refusing to resolve a name against an incomplete list "
                            "— retry, or pass the agent's uid")
                    emit(f"[warn] {name or sid} reports {int(total)} agents but stopped "
                         f"listing after {seen}; some are missing.", file=sys.stderr)
                break
            for a in agents:
                # A name is presentation; a uid is how the agent is addressed,
                # and one without it reached a KeyError further down.
                if _identifier(a.get("uid")) is None:
                    raise ProtocolError(where, "an agent has no usable uid")
                yield space, a
            seen += len(agents)
            # None means "no usable count": keep paging until a page comes
            # back empty. Treating it as 0 stopped after page one, because
            # any non-empty page already satisfies seen >= 0.
            if total is not None and seen >= total:
                break
            page += 1
        else:
            # Loop ran to MAX_PAGES with pages still outstanding. Returning
            # quietly would understate the workspace and make a name lookup
            # miss agents that exist.
            raise SystemExit(
                f"Workspace {name or sid!r} has more than {MAX_PAGES * AGENT_PAGE_SIZE} "
                f"agents ({seen} of {total} listed). Narrow with --workspace or use a uid."
            )


def resolve_agent(api, wanted, workspace=None):
    """Resolve a uid or name to a uid. Deliberately has no default.

    An account can hold agents that place real orders, so picking one on the
    user's behalf is not a convenience — it is a risk.
    """
    if not wanted:
        raise SystemExit("--agent is required (uid or name). See --list.")

    exact, fuzzy = [], []
    for space, agent in iter_agents(api, workspace):
        uid = _text(agent.get("uid")) or ""
        name = (_text(agent.get("name")) or "").strip()
        if wanted == uid:  # uids are unique — stop, don't pay for more pages
            return uid
        if wanted.lower() == name.lower():
            exact.append((space, agent, name))
        elif wanted.lower() in name.lower():
            fuzzy.append((space, agent, name))

    hits = exact or fuzzy
    if not hits:
        # Public agents are reachable by uid but absent from every listing, so
        # an unmatched value may still be valid — but only if it looks like a
        # uid. Passing an arbitrary name through would put user text into a
        # request path.
        # Say what was actually searched: with --workspace only that one was.
        scope = f"workspace {workspace!r}" if workspace else "any of your workspaces"
        if UID_RE.fullmatch(wanted):
            emit(f"[warn] {wanted!r} was not found in {scope}; trying it as a uid "
                 "(public agents are reachable but unlistable).", file=sys.stderr)
            return wanted
        raise SystemExit(
            f"No agent named {wanted!r} in {scope}. If you meant a public agent, pass "
            "its uid instead of a name — public agents cannot be listed."
        )
    if len(hits) > 1:
        listing = "\n".join(
            f"  - {n}  uid={_text(a.get('uid')) or '?'}  "
            f"(workspace={_text(s.get('name')) or '?'})"
            for s, a, n in hits
        )
        raise SystemExit(f"{wanted!r} matches several agents — pass a uid:\n{listing}")
    return hits[0][1]["uid"]


# ---------------------------------------------------------------- sse


def iter_events(resp):
    """Yield (event_name, data) per SSE frame.

    Two details that a line-at-a-time reader gets wrong. A frame ends at a
    blank line, not at each `data:` line — the spec allows a payload split
    across several `data:` lines, which must be rejoined with newlines before
    parsing, or every piece is discarded as malformed JSON. And the real event
    type lives in the payload's `event` field: the SSE `event:` line is always
    `message`, so dispatching on it collapses ~23 types into one.
    """
    buffer = []

    def flush():
        if not buffer:
            return None
        chunk = "\n".join(buffer).strip()
        buffer.clear()
        if not chunk or chunk == "[DONE]":
            return None
        try:
            frame = json.loads(chunk)
        except ValueError:
            # A frame we cannot parse means the answer we assemble is missing
            # something. Report it rather than returning a quietly short result.
            return "__malformed__", {"raw": chunk[:200]}
        if not isinstance(frame, dict):
            return "__malformed__", {"raw": chunk[:200]}
        event = frame.get("event")
        if not isinstance(event, str) or not event:
            event = "other"
        if event == "ping":
            # Keepalive, carries nothing. Dropping it here keeps it out of the
            # event counts and out of the malformed tally — it has no `data`
            # field, so shape-checking every frame had been reporting each
            # heartbeat as lost content.
            return None
        data = frame.get("data")
        if not isinstance(data, dict):
            return "__malformed__", {"raw": chunk[:200]}
        return event, data

    for raw in resp:
        line = raw.decode("utf-8", "replace").rstrip("\r\n")
        if not line:  # frame delimiter
            if (event := flush()) is not None:
                yield event
            continue
        if line.startswith("data:"):
            buffer.append(line[5:].lstrip())
    if (event := flush()) is not None:  # stream ended without a trailing blank
        yield event


def consume(resp, progress=True):
    """Fold a stream into one result.

    Four things the shape of the stream forces:
      * `message` carries three kinds of text — answer / think / process.
        Mixing them puts the model's reasoning into the answer.
      * An interrupted run never sends `workflow_finished`, only
        `human_interaction_required`.
      * `workflow_finished` omits the ids; they come from `chat_started`.
      * `workflow_finished` is not always the last frame — read to the end.
    """
    out = {"answer": "", "status": None, "events": {}}
    answer, thinking = [], []
    echo = _Echo(sys.stderr)

    # The guard wraps the `with`, not the reverse: a stream can die mid-answer,
    # and closing the response can fail too. Either way, keep what arrived and
    # mark it incomplete — letting the exception escape would print a traceback
    # over text the user just watched being typed out.
    try:
        with resp:
            for kind, data in iter_events(resp):
                out["events"][kind] = out["events"].get(kind, 0) + 1

                if kind == "message":
                    # Server-supplied; a number here would break "".join() later.
                    text = data.get("text")
                    text = text if isinstance(text, str) else ""
                    # Only an explicit `type: "answer"` is answer text — the
                    # reference implementation (the CLI, live-tested) treats
                    # everything else, missing included, as progress noise.
                    # Defaulting the missing case to "answer" would let a new
                    # server-side message kind leak into the answer verbatim.
                    mtype = data.get("type")
                    if mtype == "answer":
                        answer.append(text)
                        if progress and text:
                            echo.write(text)
                    elif mtype == "think":
                        thinking.append(text)

                elif kind == "chat_started":
                    out["chat_uid"] = data.get("chat_uid")
                    out["message_id"] = data.get("message_id")

                elif kind in ("workflow_finished", "human_interaction_required"):
                    out["status"] = data.get("status") or (
                        "interrupted" if kind == "human_interaction_required" else None
                    )
                    # The reference parser keeps this field (events.rs); a
                    # failed run without a later chat_finished otherwise
                    # rendered "failed" with the server's explanation dropped.
                    if err := _text(data.get("error_message")):
                        out["failure"] = err
                    outputs = data.get("outputs")
                    if not isinstance(outputs, dict):
                        outputs = {}
                    # Server-supplied and read as text or lists later: a number
                    # here breaks .strip(), a list breaks .get().
                    final = outputs.get("answer") or data.get("answer")
                    if isinstance(final, str) and final:
                        out["answer"] = final
                    refs, dropped = _objects(outputs.get("references")
                                             or data.get("references"))
                    out["references"] = refs or None
                    if dropped:
                        out["malformed"] = out.get("malformed", 0) + dropped
                    # The interrupt payload sits at the frame's top level:
                    # `tool_call_id` and `questions` are siblings of `status`,
                    # not children of an `interrupt` key. Reading a nested
                    # `interrupt` object — never present on the live wire —
                    # made every interrupted run render with no questions and
                    # no resume ids. The nested shape is kept only as a
                    # fallback in case another deployment wraps it.
                    nested = data.get("interrupt")
                    source = nested if isinstance(nested, dict) else data
                    if source.get("questions") is not None or source.get("tool_call_id"):
                        # Normalize members too: a list that contains
                        # strings passed the container check and then broke
                        # the renderer.
                        questions, bad_q = _objects(source.get("questions"))
                        for q in questions:
                            opts, bad_o = _objects(q.get("options"))
                            q["options"] = opts
                            bad_q += bad_o
                        out["interrupt"] = {
                            "tool_call_id": source.get("tool_call_id"),
                            "questions": questions,
                        }
                        if bad_q:
                            out["malformed"] = out.get("malformed", 0) + bad_q
                    if kind == "human_interaction_required":
                        # Terminal for this run: the agent is waiting on us, so
                        # nothing more is coming. Keep reading past
                        # workflow_finished (later frames still carry ids), but not
                        # past this one — the server may hold the connection open
                        # and we would block forever on a run already answered.
                        break

                elif kind == "chat_finished":
                    # Only if nothing more specific was recorded: the
                    # reference aggregator keeps the workflow_finished
                    # reason and treats this as a fallback, and a probe
                    # showed the generic teardown text replacing it.
                    if not out.get("failure"):
                        if err := (data.get("error_message") or data.get("error")):
                            out["failure"] = err

                elif kind == "__malformed__":
                    out["malformed"] = out.get("malformed", 0) + 1
    except TRANSPORT_ERRORS as exc:
        # Not `str(exc)`: `http.client` builds its messages out of the bytes it
        # choked on, so a status line containing a token reproduced it here.
        out["transport_error"] = _safe_reason(exc)

    echo.close()
    if progress and (answer or thinking):
        emit(file=sys.stderr)
    if not out["answer"]:
        out["answer"] = "".join(answer)  # only the answer stream, never think
    out["thinking"] = "".join(thinking).strip()
    if out["status"] is None:
        # The stream ended without a terminal event. Whatever text arrived is a
        # fragment; presenting it as the answer would hide the truncation.
        out["status"] = "unknown"
        out["truncated"] = True
    return out


# ---------------------------------------------------------------- render


def _sh(value):
    """Single-quote `value` for a copy-pasteable POSIX shell line.

    `shlex.quote` leaves "safe-looking" strings unquoted, which makes the
    hint's shape depend on the data; quoting always is simpler to test and
    to read. Embedded single quotes become `'\''`, exactly as the reference
    CLI's shell_single_quote does.
    """
    text = str(value if value is not None else "")
    return "'" + text.replace("'", "'\\''") + "'"


def render(result, question):
    out = [f"**Q**: {question}", ""]

    if interrupt := result.get("interrupt"):
        out += ["## The agent needs more information", ""]
        for i, q in enumerate(interrupt.get("questions") or [], 1):
            kind = "multi-select" if q.get("multi_select") else "single"
            out.append(f"{i}. {q.get('question')}  ({kind})")
            for opt in q.get("options") or []:
                out.append(f"   - {opt.get('description')}")
        # The hint must survive being followed literally. It deliberately
        # carries no --answer template: any shell-quoted blank would have to
        # be hand-edited inside quotes, and a plain "I don't know" typed
        # there breaks the command line. Run as printed, the script asks the
        # cached questions back and reads the answers with no shell in
        # between. Every id is still shell-quoted (server text), exactly as
        # the reference CLI quotes it.
        out += [
            "",
            "Resume with: `--agent " + _sh(result.get("agent") or "<UID>")
            + " --continue " + _sh(result.get("chat_uid"))
            + " --message-id " + _sh(result.get("message_id"))
            + " --tool-call-id " + _sh(interrupt.get("tool_call_id")) + "`",
            "",
            "It will ask these questions again, one per line. Scripts can add "
            "--answer '<JSON object of question: answer>' to skip the prompts.",
            "",
        ]

    # Anything short of success is stated up front. A partial answer under a
    # failed run must not read like a complete one.
    status = result.get("status")
    if status not in ("succeeded", "interrupted", None):
        out += [f"> ⚠️ Run status: **{status}**"
                + (f" — {result['failure']}" if result.get("failure") else ""), ""]
    if err := result.get("transport_error"):
        out += [f"> ⚠️ The connection dropped mid-answer ({err}). What follows is "
                "only the part that arrived.", ""]
    elif result.get("truncated"):
        out += ["> ⚠️ The stream ended without a completion event — the answer below "
                "may be cut short. Re-run to get a complete one.", ""]
    if n := result.get("malformed"):
        out += [f"> ⚠️ {n} unusable item(s) were dropped; the answer may be "
                "missing content.", ""]

    if answer := (result.get("answer") or "").strip():
        out += [answer, ""]
    elif not result.get("interrupt"):
        out += ["_(empty answer)_", ""]
        if not result.get("events", {}).get("message"):
            out += ["> No message events arrived — the token may lack AI access, "
                    "or the agent may not be conversational.", ""]
        # The failure line is only added here when the status banner above did
        # not already carry it, so it is never printed twice.
        if (failure := result.get("failure")) and status in ("succeeded", "interrupted", None):
            out += [f"> {failure}", ""]

    if refs := result.get("references"):
        out += ["## Sources", ""]
        out += [f"- [{r.get('index', '-')}] {r.get('title') or ''} {r.get('url') or ''}".rstrip()
                for r in refs]
        out.append("")

    if url := _conversation_url(result.get("chat_uid")):
        # A terminal cannot render the charts and quote cards an answer may
        # carry, and cannot be scrolled back to later the way a page can.
        # Offer the same conversation on the web, right under the answer.
        out += [f"Open on the web: {url}", ""]

    if result.get("chat_uid"):
        out += [
            f"chat_uid: `{result['chat_uid']}`  message_id: `{result.get('message_id')}`",
            "",
            "> Follow up with BOTH ids. `--chat-uid` alone only files the message "
            "under the same conversation; `--parent-message-id` is what carries the "
            "previous turn into the agent's context. Each round's message_id becomes "
            "the next round's parent.",
        ]
    return "\n".join(out).rstrip() + "\n"


def _conversation_url(chat_uid):
    """The browser URL for a conversation, or None if the id is unusable.

    The id goes into a path, so it is validated exactly as one bound for a
    request — a stray value must not build a link to somewhere else.
    """
    chat = _identifier(chat_uid)
    return CONVERSATION_URL + chat if chat else None


# ---------------------------------------------------------------- cli


def main():
    p = _Parser(
        description="Talk to a Longbridge AI agent (fallback for when the CLI is absent)."
    )
    # Actions get short names; anything naming an API field keeps the field's
    # own name, so what you pass and what the server calls it stay the same.
    p.add_argument("query", nargs="?", help="the question to ask")
    p.add_argument("--agent", help="agent uid or name (required; no default)")
    p.add_argument("--list", action="store_true", help="list agents and exit")
    p.add_argument("--workspace", help="limit to one workspace (name or id)")
    p.add_argument("--chat-uid", help="continue an existing conversation")
    p.add_argument("--parent-message-id", help="previous round's message_id")
    # `continue` is a Python keyword, so the attribute needs an explicit dest.
    p.add_argument("--continue", dest="continue_chat", metavar="CHAT_UID",
                   help="answer an interrupted run: its chat_uid")
    p.add_argument("--message-id", help="the interrupted run's message_id")
    p.add_argument("--tool-call-id", help="the interrupt's tool_call_id")
    p.add_argument("--answer", action="append", default=[], help="'question=answer', repeatable")
    p.add_argument("--json", action="store_true", help="print the raw result as JSON")
    p.add_argument("--quiet", action="store_true", help="do not stream to stderr")
    p.add_argument("--client-id", help="OAuth client_id (or LONGBRIDGE_CLIENT_ID)")
    p.add_argument("--login", action="store_true", help="force re-authorization")
    args = p.parse_args()

    api = Api(access_token(_client_id(args.client_id), force_login=args.login))

    if args.list:
        current = None
        for space, agent in iter_agents(api, args.workspace, partial=True):
            if space.get("id") != current:
                current = space.get("id")
                emit(f"\nWorkspace: {space.get('name')} (id={current})")
            desc = (_text(agent.get("description")) or "").replace("\n", " ")[:60]
            emit(f"  - {agent.get('name')}  uid={agent.get('uid')}  {desc}")
        return

    if not args.query and not args.continue_chat:
        p.error("need a query, or --continue to resume an interrupted run")

    agent = resolve_agent(api, args.agent, args.workspace)

    if args.continue_chat:
        if not (args.message_id and args.tool_call_id):
            p.error("--continue needs --message-id and --tool-call-id")
        answers = (_parse_answers(args.answer, p.error) if args.answer
                   else _ask_answers(args.continue_chat, args.message_id, p.error))
        path = (f"/v1/ai/agents/{_seg(agent)}/conversations/{_seg(args.continue_chat)}"
                f"/messages/{_seg(args.message_id)}/continue")
        body = {"answers_by_tool_call": {args.tool_call_id: answers}}
        label = f"(resuming {args.continue_chat})"
    else:
        path = f"/v1/ai/agents/{_seg(agent)}/conversations"
        body = {"query": args.query}
        if args.chat_uid:
            body["chat_uid"] = args.chat_uid
            if not args.parent_message_id:
                emit("[warn] --chat-uid without --parent-message-id: the agent will "
                     "not see the previous turn.", file=sys.stderr)
        if args.parent_message_id:
            if not args.chat_uid:
                p.error("--parent-message-id requires --chat-uid")
            body["parent_message_id"] = str(args.parent_message_id).strip()
        label = args.query

    result = consume(api.post_sse(path, body), progress=not args.quiet)
    result["agent"] = agent  # so the resume hint can name it
    if args.continue_chat:
        _backfill_ids(result, args.continue_chat, args.message_id)
    if result.get("interrupt"):
        _save_interrupt(result)
    if url := _conversation_url(result.get("chat_uid")):
        result["web_url"] = url  # so --json callers need not rebuild it
    if args.json:
        # Sanitised before encoding, not after: rewriting the encoded text
        # would change what the JSON decodes to.
        sys.stdout.write(json.dumps(_clean(result), ensure_ascii=False, indent=2) + "\n")
    else:
        emit(render(result, label), end="")


class _Parser(argparse.ArgumentParser):
    """argparse, routed through `emit`.

    argparse writes usage, help and errors to the terminal itself. That was
    the last path out of this program that did not pass the output gate: an
    unknown option containing an escape sequence was echoed back verbatim.
    """

    def _print_message(self, message, file=None):
        if message:
            emit(message, file=file or sys.stderr, end="")


def _interrupt_cache_path(chat_uid, message_id):
    """Cache file for one interrupted run, or None if the ids are unusable.

    Both components are server-supplied; validating them is what keeps this
    from being a path-injection primitive.
    """
    chat, msg = _identifier(chat_uid), _identifier(message_id)
    if chat is None or msg is None:
        return None
    return INTERRUPT_CACHE / f"{chat}-{msg}.json"


def _backfill_ids(result, chat_uid, message_id):
    """Fill missing chat/message ids from the request that was just made.

    /continue resumes an existing conversation and may skip re-announcing
    its identity with chat_started (observed live; the reference CLI
    backfills for the same reason). Without these, a second interrupt in
    the resumed run renders a hint with empty ids and caches to no path.
    A real chat_started always wins — only empty fields are touched.
    """
    if not result.get("chat_uid"):
        result["chat_uid"] = chat_uid
    if not result.get("message_id"):
        result["message_id"] = message_id


def _save_interrupt(result):
    """Remember what an interrupted run asked.

    The answers the server accepts are keyed by the question texts, and the
    continue command runs in a fresh process that has no other way to learn
    them. Failure to cache is not failure to run — the printed hint and
    --answer JSON still work — so errors are swallowed.
    """
    interrupt = result.get("interrupt") or {}
    path = _interrupt_cache_path(result.get("chat_uid"), result.get("message_id"))
    # `.strip()` decides emptiness only. The cached text must be the
    # question exactly as asked — it is the key the server matches answers
    # against, and a trimmed copy of "  Is P/E=20 acceptable?  " is a
    # different key the server ignores.
    questions = [q for q in (_text(x.get("question"))
                             for x in interrupt.get("questions") or [])
                 if q and q.strip()]
    if path is None or not questions:
        return
    try:
        _write_secret(path, {"tool_call_id": interrupt.get("tool_call_id"),
                             "questions": questions})
    except SystemExit:
        # _write_secret treats an unwritable disk as fatal, which is right
        # for a token and wrong here: the cache is a convenience, and a
        # read-only container must not lose a perfectly good interrupt
        # before it is even rendered.
        emit("[warn] could not cache the questions on this machine; resume "
             "with --answer '{\"<question>\": \"<answer>\"}' (JSON) instead.",
             file=sys.stderr)


def _ask_answers(chat_uid, message_id, fail, ask=input):
    """Collect answers interactively, keyed to the cached questions.

    This exists because no shell-quoted template can be safely hand-edited:
    the quoting has to happen before the answer is known, and a plain
    "I don't know" typed into a single-quoted JSON blob breaks the command
    line. Read interactively, the answer never passes through a shell at
    all — quotes and backslashes arrive verbatim. (For a multi-line answer,
    or in a script, pass --answer with a JSON object instead.)
    """
    path = _interrupt_cache_path(chat_uid, message_id)
    cached = _read_json(path) if path is not None else None
    questions = (cached.get("questions") if isinstance(cached, dict) else None) or []
    questions = [q for q in questions if isinstance(q, str) and q.strip()]
    if not questions:
        fail("no --answer given, and the questions from this run are not cached "
             "on this machine. Pass --answer '{\"<question exactly as the agent "
             "asked>\": \"<answer>\"}' (JSON).")
    answers = {}
    for q in questions:
        emit(q, file=sys.stderr)
        while True:
            emit("> ", file=sys.stderr, end="")
            try:
                text = ask()
            except EOFError:
                fail("input ended before every question was answered")
            if text.strip():
                break
            emit("(empty — type an answer)", file=sys.stderr)
        answers[q] = text
    return answers


def _parse_answers(items, fail):
    """Fold repeated --answer values into {question: answer}.

    Two forms. A JSON object is exact for any text — the resume hint prints
    this form with the real questions filled in, so answering is paste-and-
    edit. 'question=answer' remains for typing by hand, split at the FIRST
    '=': a question containing '=' cannot round-trip through this form (the
    reference CLI resolves that by matching cached questions; this script is
    stateless), so it is refused with a pointer to the JSON form rather than
    silently keying the answer to a truncated question.
    """
    answers = {}
    for item in items:
        text = item.strip()
        if text.startswith("{"):
            try:
                obj = json.loads(text)
            except ValueError:
                fail(f"--answer looks like JSON but does not parse: {item!r}")
            if not isinstance(obj, dict) or not obj or not all(
                    isinstance(k, str) and isinstance(v, str) for k, v in obj.items()):
                fail("--answer JSON must be a non-empty object of strings, "
                     "{\"question\": \"answer\"}")
            answers.update(obj)
            continue
        key, sep, value = text.partition("=")
        if not sep or not key.strip():
            fail(f"--answer must be 'question=answer' or a JSON object, got {item!r}")
        if "=" in value:
            # Ambiguous: there is no way to tell which '=' separates the
            # question from the answer, so no concrete split can be
            # suggested — a guessed one reads authoritative and sends an
            # answer keyed to a question the agent never asked. Point at
            # the resume hint, which prints the exact questions as JSON.
            fail(f"{item!r} contains more than one '=' and the split is "
                 "ambiguous. Copy the JSON form from the Resume hint and "
                 "fill in your answer: --answer '{\"<question exactly as "
                 "printed>\": \"<answer>\"}'")
        answers[key.strip()] = value.strip()
    return answers


def _cli():
    try:
        main()
    except (ApiError, TransportError, ProtocolError) as exc:
        # All three are normal outcomes (a 401, a 429, an unreachable host),
        # not bugs — report them as a message and an exit code, not a traceback.
        raise SystemExit(f"Error: {exc}") from None
    except KeyboardInterrupt:
        raise SystemExit(130) from None


if __name__ == "__main__":
    try:
        _cli()
    except SystemExit as exc:
        # Python prints a SystemExit's message itself, bypassing `emit`. Route
        # it back through the same sanitiser so that no exit path can carry a
        # terminal control sequence out inside an error message.
        raise SystemExit(_display(exc.code) if isinstance(exc.code, str)
                         else exc.code) from None
