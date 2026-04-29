#!/usr/bin/env python3
"""Longbridge K线查询 skill — CLI wrapper around `longbridge kline` /
`kline-history` / `intraday`.

Single file, stdlib only. Spawns subprocess to the local `longbridge` binary
under one of three subcommands (`kline`, `history`, `intraday`) and emits a
stable JSON envelope on stdout. All log/error output goes to stderr.

See SKILL.md for the prompt-side contract; see
docs/superpowers/specs/2026-04-28-skill-platform-protocol.md for the cross-skill
envelope and error_kind enum;
docs/superpowers/specs/2026-04-28-skill-02-kline-design.md for differential
business rules.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys


SKILL_NAME = "longbridge-kline"
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
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

AUTH_KEYWORDS = ("login", "token", "unauthorized", "auth")


def emit(payload, exit_code):
    payload.setdefault("source", "longbridge")
    payload.setdefault("skill", SKILL_NAME)
    payload.setdefault("skill_version", SKILL_VERSION)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


def emit_error(kind, message, subcommand=None, details=None, exit_code=1):
    assert kind in ERROR_KINDS, f"unknown error_kind: {kind}"
    payload = {"success": False, "error_kind": kind, "error": message}
    if subcommand is not None:
        payload["subcommand"] = subcommand
    if details is not None:
        payload["details"] = details
    emit(payload, exit_code)


def resolve_bin(arg):
    """Return absolute executable path or None."""
    if "/" in arg:
        return arg if (os.path.isfile(arg) and os.access(arg, os.X_OK)) else None
    return shutil.which(arg)


def call_longbridge(bin_path, sub, symbol, extra_args=None, timeout=30):
    """Run `longbridge <sub> <symbol> [extra] --format json`. Returns (data, error_dict_or_None)."""
    cmd = [bin_path, sub, symbol]
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


def build_parser():
    p = argparse.ArgumentParser(
        prog="cli.py",
        description="Longbridge K线查询(kline / history / intraday)",
    )
    sub = p.add_subparsers(dest="subcommand", metavar="{kline,history,intraday}")

    # kline subcommand
    sp_k = sub.add_parser("kline", help="近 N 根 K 线(默认日 K 100 根)")
    sp_k.add_argument("symbol", nargs="?", default=None,
                      help="标的代码,格式 <CODE>.<MARKET>")
    sp_k.add_argument("--period", default="day",
                      help="K 线周期:1m/5m/15m/30m/1h/day/week/month/year(默认 day)")
    sp_k.add_argument("--count", type=int, default=100,
                      help="返回根数(默认 100)")
    sp_k.add_argument("--adjust", default="no_adjust",
                      help="复权:no_adjust(默认)/ forward_adjust")
    _add_common(sp_k)

    # history subcommand
    sp_h = sub.add_parser("history", help="历史 K 线(指定起止日期)")
    sp_h.add_argument("symbol", nargs="?", default=None,
                      help="标的代码,格式 <CODE>.<MARKET>")
    sp_h.add_argument("--period", default="day",
                      help="K 线周期(默认 day)")
    sp_h.add_argument("--start", default=None, help="起始日期 YYYY-MM-DD(必填)")
    sp_h.add_argument("--end", default=None, help="终止日期 YYYY-MM-DD(必填)")
    sp_h.add_argument("--adjust", default="no_adjust",
                      help="复权:no_adjust(默认)/ forward_adjust")
    _add_common(sp_h)

    # intraday subcommand
    sp_i = sub.add_parser("intraday", help="今日分时图")
    sp_i.add_argument("symbol", nargs="?", default=None,
                      help="标的代码,格式 <CODE>.<MARKET>")
    _add_common(sp_i)

    return p


def _add_common(sp):
    sp.add_argument("--format", default="json", choices=["json"],
                    help="输出格式")
    sp.add_argument("--longbridge-bin", default="longbridge",
                    help="底层 CLI 路径,默认 'longbridge'")
    sp.add_argument("--timeout", type=int, default=30,
                    help="subprocess 超时秒数")


def emit_subprocess_error(err, subcommand):
    emit_error(
        err["kind"],
        err["message"],
        subcommand=subcommand,
        details=err.get("details"),
        exit_code=err.get("exit_code", 1),
    )


def validate_symbol(symbol, subcommand):
    if not symbol or not symbol.strip():
        emit_error(
            "no_input",
            "请告诉我要查的标的代码",
            subcommand=subcommand,
        )
    sym = symbol.strip()
    if not SYMBOL_RE.match(sym):
        emit_error(
            "invalid_input_format",
            f"代码格式不对: {sym}。要写成 <CODE>.<MARKET>,例如 NVDA.US、700.HK、600519.SH",
            subcommand=subcommand,
            details={"invalid": sym},
        )
    return sym


def validate_date(value, label, subcommand):
    if not DATE_RE.match(value):
        emit_error(
            "invalid_input_format",
            f"{label} 日期格式不对: {value}。要写成 YYYY-MM-DD,例如 2024-01-01",
            subcommand=subcommand,
            details={"invalid": value, "field": label},
        )


def run_kline(args):
    symbol = validate_symbol(args.symbol, "kline")
    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error(
            "binary_not_found",
            "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
            subcommand="kline",
            details={"path": args.longbridge_bin},
            exit_code=2,
        )
    extra = [
        "--period", args.period,
        "--count", str(args.count),
        "--adjust", args.adjust,
    ]
    data, err = call_longbridge(bin_path, "kline", symbol, extra_args=extra, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err, "kline")
    emit({
        "success": True,
        "subcommand": "kline",
        "symbol": symbol,
        "period": args.period,
        "count": args.count,
        "adjust": args.adjust,
        "datas": data if isinstance(data, list) else [],
    }, 0)


def run_history(args):
    symbol = validate_symbol(args.symbol, "history")
    # both --start and --end MUST be given together
    if not args.start or not args.end:
        missing = []
        if not args.start:
            missing.append("--start")
        if not args.end:
            missing.append("--end")
        emit_error(
            "invalid_input_format",
            f"history 子命令必须同时给出 --start 和 --end(YYYY-MM-DD)。缺少:{', '.join(missing)}。例如:--start 2024-01-01 --end 2024-12-31",
            subcommand="history",
            details={"missing": missing},
        )
    validate_date(args.start, "--start", "history")
    validate_date(args.end, "--end", "history")
    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error(
            "binary_not_found",
            "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
            subcommand="history",
            details={"path": args.longbridge_bin},
            exit_code=2,
        )
    extra = [
        "--period", args.period,
        "--start", args.start,
        "--end", args.end,
        "--adjust", args.adjust,
    ]
    data, err = call_longbridge(bin_path, "kline-history", symbol, extra_args=extra, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err, "history")
    emit({
        "success": True,
        "subcommand": "history",
        "symbol": symbol,
        "period": args.period,
        "start": args.start,
        "end": args.end,
        "adjust": args.adjust,
        "datas": data if isinstance(data, list) else [],
    }, 0)


def run_intraday(args):
    symbol = validate_symbol(args.symbol, "intraday")
    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error(
            "binary_not_found",
            "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
            subcommand="intraday",
            details={"path": args.longbridge_bin},
            exit_code=2,
        )
    data, err = call_longbridge(bin_path, "intraday", symbol, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err, "intraday")
    emit({
        "success": True,
        "subcommand": "intraday",
        "symbol": symbol,
        "datas": data if isinstance(data, list) else [],
    }, 0)


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.subcommand:
        # No subcommand at all -> treat as no_input
        emit_error(
            "no_input",
            "请告诉我要查的标的代码,以及子命令(kline / history / intraday)",
        )
    if args.subcommand == "kline":
        run_kline(args)
    elif args.subcommand == "history":
        run_history(args)
    elif args.subcommand == "intraday":
        run_intraday(args)
    else:  # pragma: no cover - argparse forbids
        parser.error(f"unknown subcommand: {args.subcommand}")


if __name__ == "__main__":
    main()
