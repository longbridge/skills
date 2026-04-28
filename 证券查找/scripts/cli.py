#!/usr/bin/env python3
"""Longbridge 证券查找 skill — 2 subcommands.

  cli.py securities    [--market HK|US|CN|SG]
  cli.py participants
"""

import argparse, json, os, shutil, subprocess, sys


SKILL_NAME = "证券查找"
SKILL_VERSION = "1.0.0"

ERROR_KINDS = {"auth_expired", "binary_not_found", "subprocess_failed",
               "no_input", "invalid_input_format", "empty_result", "risk_block"}

AUTH_KEYWORDS = ("login", "token", "unauthorized", "auth")

MARKET_ALIASES = {"HK": "HK", "US": "US", "CN": "CN", "SG": "SG", "SH": "CN", "SZ": "CN"}


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
        emit_error("invalid_input_format",
                   f"市场不支持: {arg}。可选 HK / US / CN / SG",
                   details={"market": arg})
    return MARKET_ALIASES[key]


def resolve_or_die(args):
    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error("binary_not_found",
                   "长桥 CLI 工具未安装,请先安装 longbridge-terminal",
                   details={"path": args.longbridge_bin}, exit_code=2)
    return bin_path


def _add_common(sp):
    sp.add_argument("--format", default="json", choices=["json"])
    sp.add_argument("--longbridge-bin", default="longbridge")
    sp.add_argument("--timeout", type=int, default=30)


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 证券查找")
    sub = p.add_subparsers(dest="subcommand")
    sp_s = sub.add_parser("securities", help="某市场全部证券列表")
    sp_s.add_argument("--market", default="HK")
    _add_common(sp_s)
    sp_p = sub.add_parser("participants", help="经纪商参与者字典")
    _add_common(sp_p)
    return p


def cmd_securities(args):
    market = normalize_market(args.market)
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "security-list", market, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    count = len(data) if isinstance(data, list) else 0
    emit({"success": True, "subcommand": "securities", "market": market, "count": count, "datas": data}, 0)


def cmd_participants(args):
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "participants", timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "subcommand": "participants", "datas": data}, 0)


DISPATCH = {"securities": cmd_securities, "participants": cmd_participants}


def main():
    args = build_parser().parse_args()
    if not args.subcommand:
        emit_error("no_input", "请告诉我要查什么:securities(全市场证券)/ participants(经纪商列表)")
    DISPATCH[args.subcommand](args)


if __name__ == "__main__":
    main()
