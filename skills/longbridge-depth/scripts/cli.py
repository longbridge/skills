#!/usr/bin/env python3
"""Longbridge 盘口深度 skill — CLI wrapper around `longbridge depth`/`brokers`/`trades`.

Single file, stdlib only. Spawns subprocess to the local `longbridge` binary
for one of the three micro-structure subcommands (depth / brokers / trades),
plus an `all` combo that runs depth + (brokers if HK) + trades and merges
into one envelope. All log/error output goes to stderr; stdout is JSON only.

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


SKILL_NAME = "longbridge-depth"
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

COUNT_MIN = 1
COUNT_MAX = 1000


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


def call_longbridge(bin_path, sub, positional, extra_args=None, timeout=30):
    """Run `longbridge <sub> <positional...> [extra] --format json`.

    Returns (data, error_dict_or_None).
    """
    cmd = [bin_path, sub, *positional]
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


def emit_subprocess_error(err):
    emit_error(
        err["kind"],
        err["message"],
        details=err.get("details"),
        exit_code=err.get("exit_code", 1),
    )


def _add_common(sp):
    sp.add_argument("--format", default="json", choices=["json"], help="输出格式")
    sp.add_argument("--longbridge-bin", default="longbridge",
                    help="底层 CLI 路径,默认 'longbridge'")
    sp.add_argument("--timeout", type=int, default=30,
                    help="subprocess 超时秒数")


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 盘口深度")
    sub = p.add_subparsers(dest="subcommand", metavar="{depth,brokers,trades,all}")

    sp_depth = sub.add_parser("depth", help="订单簿深度(5/10 档买卖盘)")
    sp_depth.add_argument("symbol", nargs="?", default=None, help="标的代码 <CODE>.<MARKET>")
    _add_common(sp_depth)

    sp_brokers = sub.add_parser("brokers", help="经纪商队列(仅港股)")
    sp_brokers.add_argument("symbol", nargs="?", default=None, help="标的代码,必须 .HK")
    _add_common(sp_brokers)

    sp_trades = sub.add_parser("trades", help="逐笔成交")
    sp_trades.add_argument("symbol", nargs="?", default=None, help="标的代码 <CODE>.<MARKET>")
    sp_trades.add_argument("--count", type=int, default=20,
                           help="返回笔数,1-1000,默认 20")
    _add_common(sp_trades)

    sp_all = sub.add_parser("all", help="depth + (brokers if .HK) + trades 一次取齐")
    sp_all.add_argument("symbol", nargs="?", default=None, help="标的代码 <CODE>.<MARKET>")
    sp_all.add_argument("--count", type=int, default=20,
                        help="trades 子查询的笔数,1-1000,默认 20")
    _add_common(sp_all)

    return p


def validate_symbol(symbol):
    """Returns (ok, error_message_or_None)."""
    if not symbol or not symbol.strip():
        return False, "no_input"
    if not SYMBOL_RE.match(symbol):
        return False, "invalid_format"
    return True, None


def ensure_hk(symbol):
    return symbol.endswith(".HK")


def validate_count(count):
    return COUNT_MIN <= count <= COUNT_MAX


def resolve_or_die(args):
    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error(
            "binary_not_found",
            "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
            details={"path": args.longbridge_bin},
            exit_code=2,
        )
    return bin_path


def cmd_depth(args):
    sym = args.symbol
    ok, why = validate_symbol(sym)
    if not ok:
        if why == "no_input":
            emit_error("no_input", "请告诉我要查的标的(格式 <CODE>.<MARKET>,例如 700.HK)")
        emit_error(
            "invalid_input_format",
            f"代码格式不对: {sym}。要写成 <CODE>.<MARKET>,例如 NVDA.US、700.HK、600519.SH",
            details={"invalid": sym},
        )
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "depth", [sym], timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({
        "success": True,
        "subcommand": "depth",
        "symbol": sym,
        "datas": data,
    }, 0)


def cmd_brokers(args):
    sym = args.symbol
    ok, why = validate_symbol(sym)
    if not ok:
        if why == "no_input":
            emit_error("no_input", "请告诉我要查的标的(格式 <CODE>.<MARKET>,例如 700.HK)")
        emit_error(
            "invalid_input_format",
            f"代码格式不对: {sym}。要写成 <CODE>.<MARKET>,例如 700.HK",
            details={"invalid": sym},
        )
    if not ensure_hk(sym):
        emit_error(
            "invalid_input_format",
            f"经纪商队列只支持港股(.HK),给的是 {sym}。请改用 depth 查盘口,或换成对应港股代码。",
            details={"symbol": sym, "reason": "brokers_hk_only"},
        )
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "brokers", [sym], timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({
        "success": True,
        "subcommand": "brokers",
        "symbol": sym,
        "datas": data,
    }, 0)


def cmd_trades(args):
    sym = args.symbol
    ok, why = validate_symbol(sym)
    if not ok:
        if why == "no_input":
            emit_error("no_input", "请告诉我要查的标的(格式 <CODE>.<MARKET>,例如 700.HK)")
        emit_error(
            "invalid_input_format",
            f"代码格式不对: {sym}。要写成 <CODE>.<MARKET>,例如 NVDA.US、700.HK、600519.SH",
            details={"invalid": sym},
        )
    if not validate_count(args.count):
        emit_error(
            "invalid_input_format",
            f"--count 必须在 [{COUNT_MIN}, {COUNT_MAX}] 之间,收到 {args.count}",
            details={"count": args.count, "min": COUNT_MIN, "max": COUNT_MAX},
        )
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(
        bin_path, "trades", [sym],
        extra_args=["--count", str(args.count)],
        timeout=args.timeout,
    )
    if err is not None:
        emit_subprocess_error(err)
    emit({
        "success": True,
        "subcommand": "trades",
        "symbol": sym,
        "count": args.count,
        "datas": data,
    }, 0)


def cmd_all(args):
    sym = args.symbol
    ok, why = validate_symbol(sym)
    if not ok:
        if why == "no_input":
            emit_error("no_input", "请告诉我要查的标的(格式 <CODE>.<MARKET>,例如 700.HK)")
        emit_error(
            "invalid_input_format",
            f"代码格式不对: {sym}。要写成 <CODE>.<MARKET>,例如 NVDA.US、700.HK、600519.SH",
            details={"invalid": sym},
        )
    if not validate_count(args.count):
        emit_error(
            "invalid_input_format",
            f"--count 必须在 [{COUNT_MIN}, {COUNT_MAX}] 之间,收到 {args.count}",
            details={"count": args.count, "min": COUNT_MIN, "max": COUNT_MAX},
        )
    bin_path = resolve_or_die(args)

    depth_data, err = call_longbridge(bin_path, "depth", [sym], timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)

    brokers_data = None
    if ensure_hk(sym):
        brokers_data, err = call_longbridge(bin_path, "brokers", [sym], timeout=args.timeout)
        if err is not None:
            emit_subprocess_error(err)

    trades_data, err = call_longbridge(
        bin_path, "trades", [sym],
        extra_args=["--count", str(args.count)],
        timeout=args.timeout,
    )
    if err is not None:
        emit_subprocess_error(err)

    emit({
        "success": True,
        "subcommand": "all",
        "symbol": sym,
        "count": args.count,
        "datas": {
            "depth": depth_data,
            "brokers": brokers_data,
            "trades": trades_data,
        },
    }, 0)


DISPATCH = {
    "depth": cmd_depth,
    "brokers": cmd_brokers,
    "trades": cmd_trades,
    "all": cmd_all,
}


def main():
    args = build_parser().parse_args()
    if not args.subcommand:
        emit_error(
            "no_input",
            "请告诉我要查什么:depth / brokers / trades / all 之一,加上标的代码",
        )
    DISPATCH[args.subcommand](args)


if __name__ == "__main__":
    main()
