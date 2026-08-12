# A2A API reference

Everything `scripts/agent.py` implements. You only need this file when the
`longbridge` CLI is unavailable — with the CLI, `longbridge agent --skill`
prints the authoritative version of this material and stays current
automatically.

Official docs: [发起对话](https://open.longbridge.com/zh-CN/docs/ai/chat/conversation) ·
[继续对话](https://open.longbridge.com/zh-CN/docs/ai/chat/continue) ·
[SSE 事件](https://open.longbridge.com/zh-CN/docs/ai/chat/events) ·
[Workspace 下的 Agent](https://open.longbridge.com/zh-CN/docs/ai/workspace/agents)

## Endpoints

| Purpose | Method & path |
| --- | --- |
| List workspaces | `GET /v1/ai/workspaces` |
| List a workspace's agents | `GET /v1/ai/workspaces/:id/agents` |
| Ask / follow up | `POST /v1/ai/agents/:id/conversations` |
| Answer an interrupted run | `POST /v1/ai/agents/:id/conversations/:chat_uid/messages/:message_id/continue` |

All calls take `authorization: Bearer <token>`.

**Which host.** `.cn` and `.com` are access points into the same data — a token
from one is accepted by the other. They differ in reach: the **US data center is
reachable only through `.com`**, because `.cn` has no route to it and the
`x-dc-region` header selects a data center rather than creating a route. `.com`
in turn may be unreachable from mainland-China networks. So `.cn` is the default
here, and a credential whose prefix is `us_` must be used at `.com`.

Access point (`.cn` / `.com`) and data center (`x-dc-region: ap|us`) stay
separate concepts. Ordinary API calls carry no region header at all — the
gateway routes them.

Agent listing is paginated and defaults to **20 per page** — follow `total` or a
workspace with many agents silently truncates, which breaks name lookup.

## Auth: device flow

No local callback server, so it works over SSH and in containers.

```bash
# 1. Ask for a code
curl -sS -X POST https://openapi.longbridge.cn/oauth2/device/authorize \
  -d "client_id=$CLIENT_ID"
# → {"device_code":"…","user_code":"XBJH-SFDN",
#    "verification_uri_complete":"https://open.longbridge.cn/…?user_code=XBJH-SFDN",
#    "expires_in":300,"interval":5}

# 2. Open verification_uri_complete in a browser and confirm.

# 3. Poll every `interval` seconds until it stops returning authorization_pending.
#    The code is minted on AP and replicated to US, and you cannot know in
#    advance which data center holds the account — so poll BOTH, each at a host
#    that can actually reach it. `invalid_grant` from one only means "not this
#    one"; keep polling the other until the code expires.
curl -sS -X POST https://openapi.longbridge.cn/oauth2/token \
  -H "x-dc-region: ap" \
  -d "client_id=$CLIENT_ID" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
  -d "device_code=$DEVICE_CODE"

curl -sS -X POST https://openapi.longbridge.com/oauth2/token \
  -H "x-dc-region: us" \
  -d "client_id=$CLIENT_ID" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
  -d "device_code=$DEVICE_CODE"
```

Refresh with `grant_type=refresh_token`, at the host matching the refresh
token's `us_` / `ap_` prefix. A refresh response may omit `refresh_token`,
which means keep the one you have. Only `invalid_grant` (and friends) means the
credential is dead — a 5xx is the server's problem, not a reason to make the
user authorize again.

`agent.py` caches the result at `~/.longbridge/agent-token.json` (0600) and
refreshes before expiry.

A `client_id` comes from `~/.longbridge/openapi/cli-registration` if the CLI was
ever installed, else `LONGBRIDGE_CLIENT_ID` or `--client-id`.

## Request body

```jsonc
// first round
{ "query": "分析一下 TSLA" }

// follow-up — BOTH ids required
{ "query": "那 NVDA 呢", "chat_uid": "…", "parent_message_id": "…" }

// answering an interrupted run
{ "answers_by_tool_call": { "<tool_call_id>": { "<question>": "<answer>" } } }
```

`chat_uid` alone only files the message under the same conversation; it does
**not** carry the previous turn into the agent's context, and it does not error
— the agent simply answers without the history. `parent_message_id` is what
chains the turns: each round's returned `message_id` becomes the next round's
parent.

## SSE stream

Send `accept: text/event-stream`. Four properties of the stream that a naive
reader gets wrong:

**The `event:` line is always `message`.** The real type is the `event` field
*inside* the JSON payload. Dispatching on the SSE line collapses ~23 event types
into one.

**`message` carries three kinds of text**, distinguished by `type` /
`message_type`: `answer` is the reply, `think` is the model's reasoning, and
`process` is a stage label. Concatenating them blindly leaks reasoning into the
answer.

**An interrupted run never sends `workflow_finished`** — only
`human_interaction_required`. Waiting for the former hangs.

**`workflow_finished` is not necessarily the last frame**, and it omits the ids —
`chat_uid` and `message_id` arrive in `chat_started`. Read to end of stream.

Event families: session (`chat_started`, `chat_finished`), execution
(`workflow_started`, `workflow_finished`), answer (`message`), reasoning
(`thinking_*`), tools (`node_tool_use_*`), sub-agents (`subagent_*`),
delegation (`agent_tool_*`), interruption (`human_interaction_required`), and
auxiliary (`query_masked`, `plan_changed`, `context_compress_*`).

## Interrupt payload

`questions[]` entries are **objects, not strings**:

```jsonc
{
  "tool_call_id": "call_…",
  "questions": [
    {
      "question": "回测哪个标的？",
      "multi_select": false,
      "options": [{ "description": "TQQQ — 3x long Nasdaq" }]
    }
  ]
}
```

The answer key must be the inner `question` value — not the whole object. When
`options` is non-empty, prefer one of their `description` values.

## Status and errors

`succeeded` · `interrupted` · `failed` · `stopped` · `unknown`.

| Symptom | Cause |
| --- | --- |
| `429002` | Rate limited — serialize calls, never burst |
| Empty answer, zero `message` events | Token lacks AI access, or the agent is not conversational (e.g. workflow mode) |
| `failed` with empty `error_message` | Usually a non-conversational agent |
| 404 on `/continue` | Check the path segments — `:chat_uid` and `:message_id` come from the interrupted run |

## Raw curl

```bash
# Pick the host your token belongs to: a `us_…` token only works at `.com`.
HOST=https://openapi.longbridge.cn          # AP
# HOST=https://openapi.longbridge.com       # US, or from outside mainland China

curl -sS -N -X POST "$HOST/v1/ai/agents/$UID/conversations" \
  -H "authorization: Bearer $TOKEN" \
  -H "accept: text/event-stream" \
  -H "content-type: application/json" \
  -d '{"query":"分析一下 TSLA"}'
```

Workable for a single call. Folding the stream into an answer — three text
kinds, the interrupted path, ids from a different frame — is what `agent.py`
exists for.
