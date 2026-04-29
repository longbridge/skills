#!/usr/bin/env python3
"""Longbridge 市场情绪 skill — CLI wrapper around `longbridge market-temp` /
`trading-session` / `trading-days`.

Subcommand-style:
  cli.py temp     [--market HK|US|CN|SG] [--history --start ... --end ...]
  cli.py session
  cli.py days     [--market HK|US|CN|SG] [--start ...] [--end ...]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys


SKILL_NAME = "市场情绪"
SKILL_VERSION = "1.0.0"

ERROR_KINDS = {
    "auth_expired", "binary_not_found", "subprocess_failed",
    "no_input", "invalid_input_format", "empty_result", "risk_block",
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
AUTH_KEYWORDS = ("login", "token", "unauthorized", "auth")

MARKET_ALIASES = {
    "HK": "HK", "US": "US", "CN": "CN", "SG": "SG",
    "SH": "CN", "SZ": "CN",
}


def emit(payload, exit_code):
    payload.setdefault("source", "longbridge")
    payload.setdefault("skill", SKILL_NAME)
    payload.setdefault("skill_version", SKILL_VERSION)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


def emit_error(kind, message, details=None, exit_code=1):
    assert kind in ERROR_KINDS
    payload = {"success": False, "error_kind": kind, "error": message}
    if details is not None:
        payload["details"] = details
    emit(payload, exit_code)


def resolve_bin(arg):
    if "/" in arg:
        return arg if (os.path.isfile(arg) and os.access(arg, os.X_OK)) else None
    return shutil.which(arg)


def call_longbridge(bin_path, *cmd_tail, timeout=30):
    cmd = [bin_path, *cmd_tail, "--format", "json"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, {"kind": "subprocess_failed", "message": f"查询超时({timeout}s)", "details": {"cmd": cmd}, "exit_code": 2}
    except OSError as exc:
        return None, {"kind": "subprocess_failed", "message": f"无法启动 longbridge: {exc}", "details": {"cmd": cmd, "os_error": str(exc)}, "exit_code": 2}
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        kind = "auth_expired" if any(w in stderr.lower() for w in AUTH_KEYWORDS) else "subprocess_failed"
        msg = "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权" if kind == "auth_expired" else f"longbridge 失败:{stderr or '(stderr empty)'}"
        return None, {"kind": kind, "message": msg, "details": {"cmd": cmd, "stderr": stderr, "returncode": proc.returncode}}
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError as exc:
        return None, {"kind": "subprocess_failed", "message": f"longbridge 返回不是合法 JSON: {exc}", "details": {"cmd": cmd, "stdout_head": proc.stdout[:500]}}


def emit_subprocess_error(err):
    emit_error(err["kind"], err["message"], details=err.get("details"), exit_code=err.get("exit_code", 1))


def normalize_market(arg):
    key = (arg or "HK").upper()
    if key not in MARKET_ALIASES:
        emit_error(
            "invalid_input_format",
            f"市场不支持: {arg}。可选 HK / US / CN(SH / SZ 别名为 CN)/ SG",
            details={"market": arg},
        )
    return MARKET_ALIASES[key]


def validate_date(value, label):
    if not DATE_RE.match(value):
        emit_error(
            "invalid_input_format",
            f"{label} 日期格式不对: {value}。要写成 YYYY-MM-DD",
            details={"invalid": value, "field": label},
        )


def _add_common(sp):
    sp.add_argument("--format", default="json", choices=["json"])
    sp.add_argument("--longbridge-bin", default="longbridge")
    sp.add_argument("--timeout", type=int, default=30)


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 市场情绪")
    sub = p.add_subparsers(dest="subcommand", metavar="{temp,session,days}")

    sp_t = sub.add_parser("temp", help="市场情绪温度(快照或历史)")
    sp_t.add_argument("--market", default="HK")
    sp_t.add_argument("--history", action="store_true")
    sp_t.add_argument("--start", default=None)
    sp_t.add_argument("--end", default=None)
    _add_common(sp_t)

    sp_s = sub.add_parser("session", help="所有市场的交易时段")
    _add_common(sp_s)

    sp_d = sub.add_parser("days", help="某市场的交易日历")
    sp_d.add_argument("--market", default="HK")
    sp_d.add_argument("--start", default=None)
    sp_d.add_argument("--end", default=None)
    _add_common(sp_d)

    return p


def cmd_temp(args):
    market = normalize_market(args.market)
    if args.history:
        if not args.start or not args.end:
            emit_error(
                "invalid_input_format",
                "temp --history 必须同时给 --start 和 --end(YYYY-MM-DD)",
                details={"missing": [n for n, v in [("--start", args.start), ("--end", args.end)] if not v]},
            )
        validate_date(args.start, "--start")
        validate_date(args.end, "--end")

    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error("binary_not_found",
                   "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
                   details={"path": args.longbridge_bin}, exit_code=2)

    cmd_tail = ["market-temp", market]
    if args.history:
        cmd_tail.extend(["--history", "--start", args.start, "--end", args.end])

    data, err = call_longbridge(bin_path, *cmd_tail, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)

    payload = {"success": True, "subcommand": "temp", "market": market, "datas": data}
    if args.history:
        payload["start"] = args.start
        payload["end"] = args.end
    emit(payload, 0)


def cmd_session(args):
    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error("binary_not_found",
                   "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
                   details={"path": args.longbridge_bin}, exit_code=2)
    data, err = call_longbridge(bin_path, "trading-session", timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "subcommand": "session", "datas": data}, 0)


def cmd_days(args):
    market = normalize_market(args.market)
    if args.start:
        validate_date(args.start, "--start")
    if args.end:
        validate_date(args.end, "--end")
    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error("binary_not_found",
                   "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
                   details={"path": args.longbridge_bin}, exit_code=2)
    cmd_tail = ["trading-days", market]
    if args.start:
        cmd_tail.extend(["--start", args.start])
    if args.end:
        cmd_tail.extend(["--end", args.end])
    data, err = call_longbridge(bin_path, *cmd_tail, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    payload = {"success": True, "subcommand": "days", "market": market, "datas": data}
    if args.start:
        payload["start"] = args.start
    if args.end:
        payload["end"] = args.end
    emit(payload, 0)


DISPATCH = {"temp": cmd_temp, "session": cmd_session, "days": cmd_days}


def main():
    args = build_parser().parse_args()
    if not args.subcommand:
        emit_error("no_input", "请告诉我要查什么:temp(市场情绪温度)/ session(交易时段)/ days(交易日历)")
    DISPATCH[args.subcommand](args)


if __name__ == "__main__":
    main()
