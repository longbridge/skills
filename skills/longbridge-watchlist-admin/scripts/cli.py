#!/usr/bin/env python3
"""Longbridge 自选股管理(写) skill — mutating with --confirm gate + bin lock.

  cli.py create-group <name> [--confirm]
  cli.py update-group <id> [--name <new>] [--add <s> ...] [--remove <s> ...] [--mode add|remove|replace] [--confirm]
  cli.py delete-group <id> [--purge] [--confirm]

Without --confirm: dry-run, prints plan, no subprocess to longbridge.
With --confirm: real call to longbridge. Bin must resolve to PATH-found longbridge
(no arbitrary --longbridge-bin paths to prevent fake-bin substitution attacks).
"""

import argparse, json, os, shutil, subprocess, sys


SKILL_NAME = "自选股管理"
SKILL_VERSION = "1.0.0"

ERROR_KINDS = {"auth_expired", "binary_not_found", "subprocess_failed",
               "no_input", "invalid_input_format", "empty_result", "risk_block"}

AUTH_KEYWORDS = ("login", "token", "unauthorized", "auth")
ALLOWED_MODES = {"add", "remove", "replace"}


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


def resolve_trading_bin(arg, confirming):
    """When confirming: lock to PATH-found longbridge only.

    Dry-run mode is allowed any path (so tests can use fake binary in dry-run).
    """
    if "/" in arg:
        if not (os.path.isfile(arg) and os.access(arg, os.X_OK)):
            return None
        if confirming:
            # mutating + --confirm → lock down: must be PATH-resolved longbridge
            return None
        return arg
    return shutil.which(arg)


def call_longbridge(bin_path, *cmd_tail, timeout=30):
    cmd = [bin_path, *cmd_tail, "--format", "json"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, {"kind": "subprocess_failed", "message": f"操作超时({timeout}s)", "details": {"cmd": cmd}, "exit_code": 2}
    except OSError as exc:
        return None, {"kind": "subprocess_failed", "message": f"无法启动 longbridge: {exc}", "details": {"cmd": cmd, "os_error": str(exc)}, "exit_code": 2}
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        kind = "auth_expired" if any(w in stderr.lower() for w in AUTH_KEYWORDS) else "subprocess_failed"
        msg = "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权" if kind == "auth_expired" else f"longbridge 失败:{stderr or '(stderr empty)'}"
        return None, {"kind": kind, "message": msg, "details": {"cmd": cmd, "stderr": stderr, "returncode": proc.returncode}}
    try:
        return json.loads(proc.stdout) if proc.stdout.strip() else None, None
    except json.JSONDecodeError as exc:
        return None, {"kind": "subprocess_failed", "message": f"longbridge 返回不是合法 JSON: {exc}", "details": {"cmd": cmd, "stdout_head": proc.stdout[:500]}}


def emit_subprocess_error(err):
    emit_error(err["kind"], err["message"], details=err.get("details"), exit_code=err.get("exit_code", 1))


def gate_resolve_bin(args):
    """Gate 2: locked to PATH-found longbridge when --confirm is set."""
    bin_path = resolve_trading_bin(args.longbridge_bin, args.confirm)
    if not bin_path:
        if args.confirm:
            emit_error("risk_block",
                       f"自选股管理(写)skill 在 --confirm 时只接受 PATH 上的 `longbridge`,不接受任意路径。给的是 {args.longbridge_bin}。",
                       details={"path": args.longbridge_bin, "gate": "binary_locked"},
                       exit_code=2)
        emit_error("binary_not_found",
                   "长桥 CLI 工具未安装,请先安装 longbridge-terminal",
                   details={"path": args.longbridge_bin}, exit_code=2)
    return bin_path


def _add_common(sp):
    sp.add_argument("--format", default="json", choices=["json"])
    sp.add_argument("--longbridge-bin", default="longbridge")
    sp.add_argument("--timeout", type=int, default=30)
    sp.add_argument("--confirm", action="store_true",
                    help="必须显式传此 flag 才会真正写入;否则 dry-run")


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 自选股管理(写)")
    sub = p.add_subparsers(dest="subcommand")

    sp_c = sub.add_parser("create-group", help="新建分组")
    sp_c.add_argument("name", nargs="?", default=None, help="分组名")
    _add_common(sp_c)

    sp_u = sub.add_parser("update-group", help="改名 / 加股 / 删股")
    sp_u.add_argument("group_id", nargs="?", default=None, help="分组 ID")
    sp_u.add_argument("--name", default=None, help="新分组名")
    sp_u.add_argument("--add", action="append", default=[], help="加股(可多)")
    sp_u.add_argument("--remove", action="append", default=[], help="删股(可多)")
    sp_u.add_argument("--mode", default="add", help="add / remove / replace")
    _add_common(sp_u)

    sp_d = sub.add_parser("delete-group", help="删除分组")
    sp_d.add_argument("group_id", nargs="?", default=None, help="分组 ID")
    sp_d.add_argument("--purge", action="store_true", help="同时删除分组内的股票")
    _add_common(sp_d)

    return p


def cmd_create_group(args):
    if not args.name or not args.name.strip():
        emit_error("no_input", "create-group 必须给分组名,例如 cli.py create-group \"科技股\"")

    plan = {"action": "create-group", "name": args.name}

    if not args.confirm:
        emit({
            "success": True, "dry_run": True, "subcommand": "create-group",
            "plan": plan,
            "next_step": "若用户明确确认,以完全相同的参数加 --confirm 重跑 cli.py",
        }, 0)

    bin_path = gate_resolve_bin(args)
    data, err = call_longbridge(bin_path, "watchlist", "create", args.name, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "dry_run": False, "subcommand": "create-group", "datas": data}, 0)


def cmd_update_group(args):
    if not args.group_id:
        emit_error("no_input", "update-group 必须给分组 ID(从 自选股 skill 看到)")
    mode = (args.mode or "add").lower()
    if mode not in ALLOWED_MODES:
        emit_error("invalid_input_format",
                   f"--mode 不支持: {args.mode}。可选 {sorted(ALLOWED_MODES)}",
                   details={"mode": args.mode})
    if not args.name and not args.add and not args.remove:
        emit_error("no_input", "update-group 至少需要 --name 或 --add 或 --remove 之一")

    plan = {
        "action": "update-group",
        "group_id": args.group_id,
        "rename": args.name,
        "add": list(args.add),
        "remove": list(args.remove),
        "mode": mode,
    }

    if not args.confirm:
        emit({
            "success": True, "dry_run": True, "subcommand": "update-group",
            "plan": plan,
            "next_step": "若用户明确确认,以完全相同的参数加 --confirm 重跑 cli.py",
        }, 0)

    bin_path = gate_resolve_bin(args)
    cmd_tail = ["watchlist", "update", args.group_id, "--mode", mode]
    if args.name:
        cmd_tail.extend(["--name", args.name])
    for s in args.add:
        cmd_tail.extend(["--add", s])
    for s in args.remove:
        cmd_tail.extend(["--remove", s])
    data, err = call_longbridge(bin_path, *cmd_tail, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "dry_run": False, "subcommand": "update-group", "datas": data}, 0)


def cmd_delete_group(args):
    if not args.group_id:
        emit_error("no_input", "delete-group 必须给分组 ID")

    plan = {"action": "delete-group", "group_id": args.group_id, "purge": args.purge}

    if not args.confirm:
        emit({
            "success": True, "dry_run": True, "subcommand": "delete-group",
            "plan": plan,
            "next_step": "若用户明确确认,以完全相同的参数加 --confirm 重跑 cli.py",
        }, 0)

    bin_path = gate_resolve_bin(args)
    cmd_tail = ["watchlist", "delete", args.group_id]
    if args.purge:
        cmd_tail.append("--purge")
    data, err = call_longbridge(bin_path, *cmd_tail, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "dry_run": False, "subcommand": "delete-group", "datas": data}, 0)


DISPATCH = {"create-group": cmd_create_group, "update-group": cmd_update_group, "delete-group": cmd_delete_group}


def main():
    args = build_parser().parse_args()
    if not args.subcommand:
        emit_error("no_input", "请告诉我要做什么:create-group / update-group / delete-group")
    DISPATCH[args.subcommand](args)


if __name__ == "__main__":
    main()
