#!/usr/bin/env python3
"""Longbridge 资金流向 skill — CLI wrapper around `longbridge capital-flow` / `capital-dist`.

Single file, stdlib only. Spawns subprocess to the local `longbridge` binary,
emits a stable JSON envelope on stdout. All log/error output goes to stderr.

Default: only `capital-flow` (time-series).
With `--include-dist`: also call `capital-dist` and merge into datas.distribution.

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


SKILL_NAME = "资金流向"
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


def call_longbridge(bin_path, sub, symbol, timeout=30):
    """Run `longbridge <sub> <symbol> --format json`. Returns (data, error_dict_or_None)."""
    cmd = [bin_path, sub, symbol, "--format", "json"]
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
    p = argparse.ArgumentParser(description="Longbridge 资金流向")
    p.add_argument("--symbol", "-s", action="append", default=[],
                   help="标的代码,**单个**,格式 <CODE>.<MARKET>")
    p.add_argument("--include-dist", action="store_true",
                   help="同时查询资金分布(capital-dist)")
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

    if len(symbols) > 1:
        emit_error(
            "invalid_input_format",
            "本 skill 一次只能查一只标的(底层 capital-flow / capital-dist 不支持批量),请只传一个 -s",
            details={"received": symbols},
        )

    symbol = symbols[0]
    if not SYMBOL_RE.match(symbol):
        emit_error(
            "invalid_input_format",
            f"代码格式不对: {symbol}。要写成 <CODE>.<MARKET>,例如 NVDA.US、700.HK、600519.SH",
            details={"invalid": symbol},
        )

    bin_path = resolve_bin(args.longbridge_bin)
    if not bin_path:
        emit_error(
            "binary_not_found",
            "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
            details={"path": args.longbridge_bin},
            exit_code=2,
        )

    flow_data, err = call_longbridge(bin_path, "capital-flow", symbol, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)

    datas = {"flow": flow_data}

    if args.include_dist:
        dist_data, err = call_longbridge(bin_path, "capital-dist", symbol, timeout=args.timeout)
        if err is not None:
            emit_subprocess_error(err)
        datas["distribution"] = dist_data

    emit({
        "success": True,
        "symbol": symbol,
        "datas": datas,
    }, 0)


if __name__ == "__main__":
    main()
