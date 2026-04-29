#!/usr/bin/env python3
"""Longbridge 订单与成交 skill — 4 subcommands.

  cli.py orders     [--history] [--start ...] [--end ...] [--symbol <s>]
  cli.py order      <order_id>
  cli.py executions [--history] [--start ...] [--end ...] [--symbol <s>]
  cli.py cash-flow  [--start ...] [--end ...]
"""

import argparse, json, os, re, shutil, subprocess, sys


SKILL_NAME = "订单与成交"
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
                   "长桥 CLI 工具未安装,请先安装 longbridge-terminal",
                   details={"path": args.longbridge_bin}, exit_code=2)
    return bin_path


def validate_dates(start, end):
    if start and not DATE_RE.match(start):
        emit_error("invalid_input_format",
                   f"--start 日期格式不对: {start}。要写成 YYYY-MM-DD",
                   details={"invalid": start, "field": "--start"})
    if end and not DATE_RE.match(end):
        emit_error("invalid_input_format",
                   f"--end 日期格式不对: {end}。要写成 YYYY-MM-DD",
                   details={"invalid": end, "field": "--end"})


def validate_symbol_optional(symbol):
    if symbol and not SYMBOL_RE.match(symbol):
        emit_error("invalid_input_format",
                   f"--symbol 代码格式不对: {symbol}。要写成 <CODE>.<MARKET>",
                   details={"invalid": symbol})


def _add_common(sp):
    sp.add_argument("--format", default="json", choices=["json"])
    sp.add_argument("--longbridge-bin", default="longbridge")
    sp.add_argument("--timeout", type=int, default=30)


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 订单与成交")
    sub = p.add_subparsers(dest="subcommand")

    sp_o = sub.add_parser("orders", help="今日订单或历史订单")
    sp_o.add_argument("--history", action="store_true")
    sp_o.add_argument("--start", default=None)
    sp_o.add_argument("--end", default=None)
    sp_o.add_argument("--symbol", default=None)
    _add_common(sp_o)

    sp_d = sub.add_parser("order", help="单条订单详情")
    sp_d.add_argument("order_id", nargs="?", default=None)
    _add_common(sp_d)

    sp_e = sub.add_parser("executions", help="今日成交或历史成交")
    sp_e.add_argument("--history", action="store_true")
    sp_e.add_argument("--start", default=None)
    sp_e.add_argument("--end", default=None)
    sp_e.add_argument("--symbol", default=None)
    _add_common(sp_e)

    sp_c = sub.add_parser("cash-flow", help="资金流水(出入金 / 分红 / 结算)")
    sp_c.add_argument("--start", default=None)
    sp_c.add_argument("--end", default=None)
    _add_common(sp_c)

    return p


def cmd_orders(args):
    validate_dates(args.start, args.end)
    validate_symbol_optional(args.symbol)
    bin_path = resolve_or_die(args)
    cmd_tail = ["orders"]
    if args.history:
        cmd_tail.append("--history")
    if args.start:
        cmd_tail.extend(["--start", args.start])
    if args.end:
        cmd_tail.extend(["--end", args.end])
    if args.symbol:
        cmd_tail.extend(["--symbol", args.symbol])
    data, err = call_longbridge(bin_path, *cmd_tail, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    payload = {"success": True, "subcommand": "orders", "history": args.history, "datas": data}
    if args.start:
        payload["start"] = args.start
    if args.end:
        payload["end"] = args.end
    if args.symbol:
        payload["symbol"] = args.symbol
    emit(payload, 0)


def cmd_order(args):
    if not args.order_id:
        emit_error("no_input", "请告诉我 order_id(从 orders 子命令拿,或下单后返回)")
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "order", args.order_id, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    # if longbridge returns empty for a single-fetch, upgrade to business error
    if not data or (isinstance(data, list) and len(data) == 0) or (isinstance(data, dict) and not data):
        emit_error("empty_result",
                   f"未找到订单 {args.order_id}。请确认订单 ID 是否正确。",
                   details={"subcommand": "order", "order_id": args.order_id})
    emit({"success": True, "subcommand": "order", "order_id": args.order_id, "datas": data}, 0)


def cmd_executions(args):
    validate_dates(args.start, args.end)
    validate_symbol_optional(args.symbol)
    bin_path = resolve_or_die(args)
    cmd_tail = ["executions"]
    if args.history:
        cmd_tail.append("--history")
    if args.start:
        cmd_tail.extend(["--start", args.start])
    if args.end:
        cmd_tail.extend(["--end", args.end])
    if args.symbol:
        cmd_tail.extend(["--symbol", args.symbol])
    data, err = call_longbridge(bin_path, *cmd_tail, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    payload = {"success": True, "subcommand": "executions", "history": args.history, "datas": data}
    if args.start:
        payload["start"] = args.start
    if args.end:
        payload["end"] = args.end
    if args.symbol:
        payload["symbol"] = args.symbol
    emit(payload, 0)


def cmd_cash_flow(args):
    validate_dates(args.start, args.end)
    bin_path = resolve_or_die(args)
    cmd_tail = ["cash-flow"]
    if args.start:
        cmd_tail.extend(["--start", args.start])
    if args.end:
        cmd_tail.extend(["--end", args.end])
    data, err = call_longbridge(bin_path, *cmd_tail, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    payload = {"success": True, "subcommand": "cash-flow", "datas": data}
    if args.start:
        payload["start"] = args.start
    if args.end:
        payload["end"] = args.end
    emit(payload, 0)


DISPATCH = {"orders": cmd_orders, "order": cmd_order, "executions": cmd_executions, "cash-flow": cmd_cash_flow}


def main():
    args = build_parser().parse_args()
    if not args.subcommand:
        emit_error("no_input", "请告诉我要查什么:orders / order / executions / cash-flow")
    DISPATCH[args.subcommand](args)


if __name__ == "__main__":
    main()
