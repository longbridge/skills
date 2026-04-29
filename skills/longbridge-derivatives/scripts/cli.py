#!/usr/bin/env python3
"""Longbridge 期权与窝轮 skill — 5 subcommands.

  cli.py option-quote    <contract> [<contract> ...]
  cli.py option-chain    <underlying> [--date YYYY-MM-DD]
  cli.py warrant-quote   <warrant> [<warrant> ...]
  cli.py warrant-list    <underlying>           # must be .HK
  cli.py warrant-issuers
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys


SKILL_NAME = "期权与窝轮"
SKILL_VERSION = "1.0.0"

ERROR_KINDS = {"auth_expired", "binary_not_found", "subprocess_failed",
               "no_input", "invalid_input_format", "empty_result", "risk_block"}

SYMBOL_RE = re.compile(r"^[A-Z0-9]+\.(US|HK|SH|SZ|SG)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
AUTH_KEYWORDS = ("login", "token", "unauthorized", "auth")


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


def resolve_or_die(args):
    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error("binary_not_found",
                   "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
                   details={"path": args.longbridge_bin}, exit_code=2)
    return bin_path


def validate_underlying(symbol):
    if not symbol or not symbol.strip():
        emit_error("no_input", "请告诉我要查的标的代码(<CODE>.<MARKET>)")
    if not SYMBOL_RE.match(symbol):
        emit_error("invalid_input_format",
                   f"代码格式不对: {symbol}。要写成 <CODE>.<MARKET>,例如 AAPL.US、700.HK",
                   details={"invalid": symbol})


def _add_common(sp):
    sp.add_argument("--format", default="json", choices=["json"])
    sp.add_argument("--longbridge-bin", default="longbridge")
    sp.add_argument("--timeout", type=int, default=30)


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 期权与窝轮")
    sub = p.add_subparsers(dest="subcommand")

    sp_oq = sub.add_parser("option-quote", help="期权合约报价")
    sp_oq.add_argument("contracts", nargs="*", help="OCC 期权合约符,可多个")
    _add_common(sp_oq)

    sp_oc = sub.add_parser("option-chain", help="期权链(到期日 / strike)")
    sp_oc.add_argument("underlying", nargs="?", default=None, help="底层标的 <CODE>.<MARKET>")
    sp_oc.add_argument("--date", default=None, help="到期日 YYYY-MM-DD;不给返回所有到期日")
    _add_common(sp_oc)

    sp_wq = sub.add_parser("warrant-quote", help="窝轮报价")
    sp_wq.add_argument("warrants", nargs="*", help="港股窝轮代码,可多个")
    _add_common(sp_wq)

    sp_wl = sub.add_parser("warrant-list", help="标的的窝轮列表(仅港股)")
    sp_wl.add_argument("underlying", nargs="?", default=None, help="底层标的,必须 .HK")
    _add_common(sp_wl)

    sp_wi = sub.add_parser("warrant-issuers", help="窝轮发行商列表(港股)")
    _add_common(sp_wi)

    return p


def cmd_option_quote(args):
    contracts = [c.strip() for c in args.contracts if c.strip()]
    if not contracts:
        emit_error("no_input", "请告诉我期权合约符(OCC 格式,例如 AAPL240119C190000)")
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "option-quote", *contracts, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({
        "success": True, "subcommand": "option-quote",
        "count": len(contracts), "contracts": contracts,
        "datas": data,
    }, 0)


def cmd_option_chain(args):
    validate_underlying(args.underlying)
    if args.date and not DATE_RE.match(args.date):
        emit_error("invalid_input_format",
                   f"--date 格式不对: {args.date}。要写成 YYYY-MM-DD",
                   details={"invalid": args.date})
    bin_path = resolve_or_die(args)
    if args.date:
        data, err = call_longbridge(bin_path, "option-chain", args.underlying, "--date", args.date, timeout=args.timeout)
    else:
        data, err = call_longbridge(bin_path, "option-chain", args.underlying, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    payload = {"success": True, "subcommand": "option-chain", "underlying": args.underlying, "datas": data}
    if args.date:
        payload["date"] = args.date
    emit(payload, 0)


def cmd_warrant_quote(args):
    warrants = [w.strip() for w in args.warrants if w.strip()]
    if not warrants:
        emit_error("no_input", "请告诉我窝轮代码(港股窝轮代码,如 12345.HK)")
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "warrant-quote", *warrants, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({
        "success": True, "subcommand": "warrant-quote",
        "count": len(warrants), "warrants": warrants,
        "datas": data,
    }, 0)


def cmd_warrant_list(args):
    validate_underlying(args.underlying)
    if not args.underlying.endswith(".HK"):
        emit_error("invalid_input_format",
                   f"窝轮列表只支持港股(.HK),给的是 {args.underlying}。",
                   details={"underlying": args.underlying, "reason": "warrant_hk_only"})
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "warrant-list", args.underlying, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "subcommand": "warrant-list", "underlying": args.underlying, "datas": data}, 0)


def cmd_warrant_issuers(args):
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "warrant-issuers", timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "subcommand": "warrant-issuers", "datas": data}, 0)


DISPATCH = {
    "option-quote": cmd_option_quote,
    "option-chain": cmd_option_chain,
    "warrant-quote": cmd_warrant_quote,
    "warrant-list": cmd_warrant_list,
    "warrant-issuers": cmd_warrant_issuers,
}


def main():
    args = build_parser().parse_args()
    if not args.subcommand:
        emit_error("no_input",
                   "请告诉我要查什么:option-quote / option-chain / warrant-quote / warrant-list / warrant-issuers")
    DISPATCH[args.subcommand](args)


if __name__ == "__main__":
    main()
