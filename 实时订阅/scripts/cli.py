#!/usr/bin/env python3
"""Longbridge 实时订阅 skill — wraps `longbridge subscriptions` (no params)."""

import argparse, json, os, shutil, subprocess, sys


SKILL_NAME = "实时订阅"
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


def main():
    p = argparse.ArgumentParser(description="Longbridge 实时订阅")
    p.add_argument("--format", default="json", choices=["json"])
    p.add_argument("--longbridge-bin", default="longbridge")
    p.add_argument("--timeout", type=int, default=30)
    args = p.parse_args()

    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error("binary_not_found",
                   "长桥 CLI 工具未安装,请先安装 longbridge-terminal",
                   details={"path": args.longbridge_bin}, exit_code=2)

    cmd = [bin_path, "subscriptions", "--format", "json"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        emit_error("subprocess_failed", f"查询超时({args.timeout}s)", details={"cmd": cmd}, exit_code=2)
    except OSError as exc:
        emit_error("subprocess_failed", f"无法启动 longbridge: {exc}", details={"cmd": cmd, "os_error": str(exc)}, exit_code=2)

    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        kind = "auth_expired" if any(w in stderr.lower() for w in AUTH_KEYWORDS) else "subprocess_failed"
        msg = "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权" if kind == "auth_expired" else f"longbridge 失败:{stderr or '(stderr empty)'}"
        emit_error(kind, msg, details={"cmd": cmd, "stderr": stderr, "returncode": proc.returncode}, exit_code=1)

    try:
        data = json.loads(proc.stdout) if proc.stdout.strip() else []
    except json.JSONDecodeError as exc:
        emit_error("subprocess_failed", f"longbridge 返回不是合法 JSON: {exc}",
                   details={"cmd": cmd, "stdout_head": proc.stdout[:500]})

    count = len(data) if isinstance(data, list) else 0
    emit({"success": True, "subscription_count": count, "datas": data}, 0)


if __name__ == "__main__":
    main()
