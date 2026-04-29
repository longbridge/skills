#!/usr/bin/env python3
"""Longbridge 持仓查询 skill — 6 subcommands.

  cli.py portfolio                                    # combo of positions + funds + balance
  cli.py positions
  cli.py funds                                        # alias for fund-positions
  cli.py balance       [--currency USD|HKD|CNY|SGD]
  cli.py margin-ratio  <symbol>
  cli.py max-qty       <symbol> --side buy|sell [--price ...] [--order-type LO|MO|...]
"""

import argparse, json, os, re, shutil, subprocess, sys


SKILL_NAME = "longbridge-positions"
SKILL_VERSION = "1.0.0"

ERROR_KINDS = {"auth_expired", "binary_not_found", "subprocess_failed",
               "no_input", "invalid_input_format", "empty_result", "risk_block"}

SYMBOL_RE = re.compile(r"^[A-Z0-9]+\.(US|HK|SH|SZ|SG)$")
AUTH_KEYWORDS = ("login", "token", "unauthorized", "auth")
ALLOWED_CURRENCIES = {"USD", "HKD", "CNY", "SGD"}
ALLOWED_SIDES = {"buy", "sell"}
ALLOWED_ORDER_TYPES = {"LO", "MO", "ELO", "ALO"}
LO_LIKE = {"LO", "ELO", "ALO"}


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


def validate_symbol_or_die(symbol):
    if not symbol or not symbol.strip():
        emit_error("no_input", "请告诉我要查的标的代码 (<CODE>.<MARKET>)")
    if not SYMBOL_RE.match(symbol):
        emit_error("invalid_input_format",
                   f"代码格式不对: {symbol}。要写成 <CODE>.<MARKET>",
                   details={"invalid": symbol})


def _add_common(sp):
    sp.add_argument("--format", default="json", choices=["json"])
    sp.add_argument("--longbridge-bin", default="longbridge")
    sp.add_argument("--timeout", type=int, default=30)


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 持仓查询")
    sub = p.add_subparsers(dest="subcommand")

    sp_pf = sub.add_parser("portfolio", help="持仓 + 基金 + 余额 一次取齐")
    _add_common(sp_pf)

    sp_p = sub.add_parser("positions", help="股票持仓")
    _add_common(sp_p)

    sp_f = sub.add_parser("funds", help="基金持仓(等同 fund-positions)")
    _add_common(sp_f)

    sp_b = sub.add_parser("balance", help="账户余额")
    sp_b.add_argument("--currency", default=None, help="可选 USD/HKD/CNY/SGD")
    _add_common(sp_b)

    sp_m = sub.add_parser("margin-ratio", help="某标的保证金率")
    sp_m.add_argument("symbol", nargs="?", default=None, help="标的代码 <CODE>.<MARKET>")
    _add_common(sp_m)

    sp_q = sub.add_parser("max-qty", help="估算可买/可卖最大数量")
    sp_q.add_argument("symbol", nargs="?", default=None, help="标的代码 <CODE>.<MARKET>")
    sp_q.add_argument("--side", default=None, help="buy / sell")
    sp_q.add_argument("--price", default=None, help="限价(LO/ELO/ALO 必填)")
    sp_q.add_argument("--order-type", default="LO", help="LO(默认)/ MO / ELO / ALO")
    _add_common(sp_q)

    return p


def cmd_portfolio(args):
    bin_path = resolve_or_die(args)
    pos, err = call_longbridge(bin_path, "positions", timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    funds, err = call_longbridge(bin_path, "fund-positions", timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    bal, err = call_longbridge(bin_path, "balance", timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({
        "success": True, "subcommand": "portfolio",
        "datas": {"positions": pos, "fund_positions": funds, "balance": bal},
    }, 0)


def cmd_positions(args):
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "positions", timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "subcommand": "positions", "datas": data}, 0)


def cmd_funds(args):
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "fund-positions", timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "subcommand": "funds", "datas": data}, 0)


def cmd_balance(args):
    if args.currency is not None:
        cur = args.currency.upper()
        if cur not in ALLOWED_CURRENCIES:
            emit_error("invalid_input_format",
                       f"--currency 不支持: {args.currency}。可选 {sorted(ALLOWED_CURRENCIES)}",
                       details={"currency": args.currency})
    bin_path = resolve_or_die(args)
    cmd_tail = ["balance"]
    if args.currency:
        cmd_tail.extend(["--currency", args.currency.upper()])
    data, err = call_longbridge(bin_path, *cmd_tail, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    payload = {"success": True, "subcommand": "balance", "datas": data}
    if args.currency:
        payload["currency"] = args.currency.upper()
    emit(payload, 0)


def cmd_margin_ratio(args):
    validate_symbol_or_die(args.symbol)
    bin_path = resolve_or_die(args)
    data, err = call_longbridge(bin_path, "margin-ratio", args.symbol, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    emit({"success": True, "subcommand": "margin-ratio", "symbol": args.symbol, "datas": data}, 0)


def cmd_max_qty(args):
    validate_symbol_or_die(args.symbol)
    if not args.side:
        emit_error("no_input", "max-qty 必须给 --side buy 或 sell")
    side = args.side.lower()
    if side not in ALLOWED_SIDES:
        emit_error("invalid_input_format",
                   f"--side 不支持: {args.side}。可选 buy / sell",
                   details={"side": args.side})
    order_type = (args.order_type or "LO").upper()
    if order_type not in ALLOWED_ORDER_TYPES:
        emit_error("invalid_input_format",
                   f"--order-type 不支持: {args.order_type}。可选 LO / MO / ELO / ALO",
                   details={"order_type": args.order_type})
    if order_type in LO_LIKE and not args.price:
        emit_error("invalid_input_format",
                   f"{order_type} 订单必须给 --price",
                   details={"order_type": order_type, "missing": "--price"})

    bin_path = resolve_or_die(args)
    cmd_tail = ["max-qty", args.symbol, "--side", side, "--order-type", order_type]
    if args.price:
        cmd_tail.extend(["--price", args.price])
    data, err = call_longbridge(bin_path, *cmd_tail, timeout=args.timeout)
    if err is not None:
        emit_subprocess_error(err)
    payload = {
        "success": True, "subcommand": "max-qty",
        "symbol": args.symbol, "side": side, "order_type": order_type,
        "datas": data,
    }
    if args.price:
        payload["price"] = args.price
    emit(payload, 0)


DISPATCH = {
    "portfolio": cmd_portfolio,
    "positions": cmd_positions,
    "funds": cmd_funds,
    "balance": cmd_balance,
    "margin-ratio": cmd_margin_ratio,
    "max-qty": cmd_max_qty,
}


def main():
    args = build_parser().parse_args()
    if not args.subcommand:
        emit_error("no_input",
                   "请告诉我要查什么:portfolio / positions / funds / balance / margin-ratio / max-qty")
    DISPATCH[args.subcommand](args)


if __name__ == "__main__":
    main()
