#!/usr/bin/env python3
"""Longbridge 行情查询 skill — CLI wrapper around `longbridge quote`/`static`/`calc-index`.

Single file, stdlib only. Spawns subprocess to the local `longbridge` binary,
merges quote / static / calc-index outputs by symbol, emits a stable JSON
envelope on stdout. All log/error output goes to stderr.

See SKILL.md for the prompt-side contract; see
docs/superpowers/specs/2026-04-28-skill-platform-protocol.md for the cross-skill
envelope and error_kind enum.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys


SKILL_NAME = "longbridge-quote"
SKILL_VERSION = "1.0.0"

ERROR_KINDS = {
    "auth_expired",
    "binary_not_found",
    "subprocess_failed",
    "no_input",
    "invalid_input_format",
    "empty_result",
    "risk_block",
}

SYMBOL_RE = re.compile(r"^[A-Z0-9]+\.(US|HK|SH|SZ|SG)$")

AUTH_KEYWORDS = ("login", "token", "unauthorized", "auth")


def emit(payload, exit_code):
    payload.setdefault("source", "longbridge")
    payload.setdefault("skill", SKILL_NAME)
    payload.setdefault("skill_version", SKILL_VERSION)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


def emit_error(kind, message, details=None, exit_code=1):
    assert kind in ERROR_KINDS, f"unknown error_kind: {kind}"
    payload = {"success": False, "error_kind": kind, "error": message}
    if details is not None:
        payload["details"] = details
    emit(payload, exit_code)


def resolve_bin(arg):
    """Return absolute executable path or None."""
    if "/" in arg:
        return arg if (os.path.isfile(arg) and os.access(arg, os.X_OK)) else None
    return shutil.which(arg)


def call_longbridge(bin_path, sub, symbols, extra_args=None, timeout=30):
    """Run `longbridge <sub> <symbols...> [extra] --format json`. Returns (data, error_dict_or_None)."""
    cmd = [bin_path, sub, *symbols]
    if extra_args:
        cmd.extend(extra_args)
    cmd.extend(["--format", "json"])
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, {
            "kind": "subprocess_failed",
            "message": f"查询超时({timeout}s),请稍后重试",
            "details": {"cmd": cmd},
            "exit_code": 2,
        }
    except OSError as exc:
        return None, {
            "kind": "subprocess_failed",
            "message": f"无法启动 longbridge: {exc}",
            "details": {"cmd": cmd, "os_error": str(exc)},
            "exit_code": 2,
        }
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        kind = (
            "auth_expired"
            if any(w in stderr.lower() for w in AUTH_KEYWORDS)
            else "subprocess_failed"
        )
        msg = (
            "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权"
            if kind == "auth_expired"
            else f"longbridge {sub} 失败:{stderr or '(stderr empty)'}"
        )
        return None, {
            "kind": kind,
            "message": msg,
            "details": {"cmd": cmd, "stderr": stderr, "returncode": proc.returncode},
        }
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError as exc:
        return None, {
            "kind": "subprocess_failed",
            "message": f"longbridge 返回不是合法 JSON: {exc}",
            "details": {"cmd": cmd, "stdout_head": proc.stdout[:500]},
        }


def by_symbol(items):
    """Build {symbol: item} from a list of dicts that each have a 'symbol' key."""
    return {it.get("symbol"): it for it in (items or []) if isinstance(it, dict)}


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 行情查询")
    p.add_argument("--symbol", "-s", action="append", default=[],
                   help="标的代码,可多次,格式 <CODE>.<MARKET>")
    p.add_argument("--include-static", action="store_true",
                   help="同时查询静态参考信息")
    p.add_argument("--index", default="",
                   help="估值指标,逗号分隔(如 pe,pb,turnover_rate)。非空时调 calc-index")
    p.add_argument("--format", default="json", choices=["json"],
                   help="输出格式")
    p.add_argument("--longbridge-bin", default="longbridge",
                   help="底层 CLI 路径,默认 'longbridge'")
    p.add_argument("--timeout", type=int, default=30,
                   help="subprocess 超时秒数")
    return p


def emit_subprocess_error(err):
    emit_error(
        err["kind"],
        err["message"],
        details=err.get("details"),
        exit_code=err.get("exit_code", 1),
    )


def main():
    args = build_parser().parse_args()
    symbols = [s.strip() for s in args.symbol if s.strip()]
    if not symbols:
        emit_error("no_input", "请告诉我要查的股票代码或公司名")

    bad = [s for s in symbols if not SYMBOL_RE.match(s)]
    if bad:
        emit_error(
            "invalid_input_format",
            f"代码格式不对: {', '.join(bad)}。要写成 <CODE>.<MARKET>,例如 NVDA.US、700.HK、600519.SH",
            details={"invalid": bad},
        )

    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error(
            "binary_not_found",
            "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
            details={"path": args.longbridge_bin},
            exit_code=2,
        )

    quote_data, err = call_longbridge(bin_path, "quote", symbols, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)

    static_data = None
    if args.include_static:
        static_data, err = call_longbridge(bin_path, "static", symbols, timeout=args.timeout)
        if err is not None:
            emit_subprocess_error(err)

    calc_data = None
    index_csv = args.index.strip()
    if index_csv:
        calc_data, err = call_longbridge(
            bin_path, "calc-index", symbols,
            extra_args=["--index", index_csv],
            timeout=args.timeout,
        )
        if err is not None:
            emit_subprocess_error(err)

    if not args.include_static and not index_csv:
        emit({
            "success": True,
            "count": len(symbols),
            "symbols": symbols,
            "datas": quote_data,
        }, 0)

    by_q = by_symbol(quote_data)
    by_s = by_symbol(static_data) if static_data is not None else {}
    by_c = by_symbol(calc_data) if calc_data is not None else {}

    merged = []
    for sym in symbols:
        item = {"symbol": sym, "quote": by_q.get(sym)}
        if args.include_static:
            item["static"] = by_s.get(sym)
        if index_csv:
            item["calc_index"] = by_c.get(sym)
        merged.append(item)

    emit({
        "success": True,
        "count": len(symbols),
        "symbols": symbols,
        "datas": merged,
    }, 0)


if __name__ == "__main__":
    main()
