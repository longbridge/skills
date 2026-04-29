#!/usr/bin/env python3
"""Longbridge 自选股(只读) skill — wraps `longbridge watchlist` (no subcommand)
with optional in-process filter by --group / --group-name.

  cli.py [--group <id>] [--group-name <name>]
"""

import argparse, json, os, shutil, subprocess, sys


SKILL_NAME = "longbridge-watchlist"
SKILL_VERSION = "1.0.0"

ERROR_KINDS = {"auth_expired", "binary_not_found", "subprocess_failed",
               "no_input", "invalid_input_format", "empty_result", "risk_block"}

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


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 自选股(只读)")
    p.add_argument("--group", default=None, help="按 group_id 过滤(精确)")
    p.add_argument("--group-name", default=None, help="按分组名过滤(包含,case-insensitive)")
    p.add_argument("--format", default="json", choices=["json"])
    p.add_argument("--longbridge-bin", default="longbridge")
    p.add_argument("--timeout", type=int, default=30)
    return p


def main():
    args = build_parser().parse_args()
    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error("binary_not_found",
                   "长桥 CLI 工具未安装,请先安装 longbridge-terminal",
                   details={"path": args.longbridge_bin}, exit_code=2)

    data, err = call_longbridge(bin_path, "watchlist", timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)

    groups = data if isinstance(data, list) else []

    # filter by group_id (精确)
    if args.group:
        groups = [g for g in groups if str(g.get("id") or g.get("group_id") or "") == str(args.group)]

    # filter by name (包含, case-insensitive)
    if args.group_name:
        needle = args.group_name.lower()
        groups = [g for g in groups if needle in str(g.get("name") or g.get("group_name") or "").lower()]

    total_symbols = sum(len(g.get("securities") or g.get("symbols") or []) for g in groups)

    emit({
        "success": True,
        "group_count": len(groups),
        "total_symbol_count": total_symbols,
        "datas": groups,
    }, 0)


if __name__ == "__main__":
    main()
