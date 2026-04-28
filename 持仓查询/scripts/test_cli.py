"""Black-box tests for 持仓查询 cli.py."""

import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLI = HERE / "cli.py"


def run_cli(*args, env=None):
    proc = subprocess.run([sys.executable, str(CLI), *args],
                          capture_output=True, text=True,
                          env={**os.environ, **(env or {})}, timeout=30)
    try:
        out = json.loads(proc.stdout) if proc.stdout.strip() else None
    except json.JSONDecodeError:
        out = None
    return proc.returncode, out, proc.stderr


def make_fake(stdout="", stderr="", exit_code=0, branches=None):
    fd, path = tempfile.mkstemp(prefix="fake-lb-", suffix=".py")
    os.close(fd)
    if branches:
        body = "import sys\nsub = sys.argv[1] if len(sys.argv) > 1 else ''\n"
        for k, v in branches.items():
            body += f"if sub == {k!r}: sys.stdout.write({v!r}); sys.exit(0)\n"
        body += "sys.stderr.write('unknown sub'); sys.exit(1)\n"
    else:
        body = f"import sys\nsys.stdout.write({stdout!r})\nsys.stderr.write({stderr!r})\nsys.exit({exit_code})\n"
    Path(path).write_text("#!/usr/bin/env python3\n" + body)
    os.chmod(path, 0o755)
    return path


class TestNoInput(unittest.TestCase):
    def test_no_subcommand(self):
        rc, out, _ = run_cli()
        self.assertEqual(out["error_kind"], "no_input")

    def test_margin_ratio_no_symbol(self):
        rc, out, _ = run_cli("margin-ratio")
        self.assertEqual(out["error_kind"], "no_input")

    def test_max_qty_no_side(self):
        rc, out, _ = run_cli("max-qty", "TSLA.US")
        self.assertEqual(out["error_kind"], "no_input")


class TestValidation(unittest.TestCase):
    def test_margin_invalid_symbol(self):
        rc, out, _ = run_cli("margin-ratio", "tsla.us")
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_max_qty_invalid_side(self):
        rc, out, _ = run_cli("max-qty", "TSLA.US", "--side", "long")
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_max_qty_lo_requires_price(self):
        rc, out, _ = run_cli("max-qty", "TSLA.US", "--side", "buy")
        self.assertEqual(out["error_kind"], "invalid_input_format")
        self.assertIn("price", out["error"].lower())

    def test_balance_invalid_currency(self):
        rc, out, _ = run_cli("balance", "--currency", "EUR")
        self.assertEqual(out["error_kind"], "invalid_input_format")


class TestBinary(unittest.TestCase):
    def test_missing(self):
        rc, out, _ = run_cli("positions", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        self.assertEqual(out["error_kind"], "binary_not_found")


class TestAuth(unittest.TestCase):
    def test_auth_expired(self):
        bp = make_fake(stderr="please login\n", exit_code=1)
        try:
            _, out, _ = run_cli("positions", "--longbridge-bin", bp)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bp)


class TestHappy(unittest.TestCase):
    def test_positions(self):
        bp = make_fake(stdout=json.dumps([{"symbol": "TSLA.US", "quantity": "100"}]))
        try:
            rc, out, _ = run_cli("positions", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "positions")
        finally:
            os.unlink(bp)

    def test_balance_with_currency(self):
        bp = make_fake(stdout=json.dumps([{"currency": "USD", "total_cash": "1000"}]))
        try:
            rc, out, _ = run_cli("balance", "--currency", "usd", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["currency"], "USD")
        finally:
            os.unlink(bp)

    def test_max_qty_lo_with_price(self):
        bp = make_fake(stdout=json.dumps({"cash_max_qty": "10", "margin_max_qty": "20"}))
        try:
            rc, out, _ = run_cli("max-qty", "TSLA.US", "--side", "buy", "--price", "250", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["side"], "buy")
            self.assertEqual(out["price"], "250")
        finally:
            os.unlink(bp)

    def test_max_qty_mo_no_price(self):
        bp = make_fake(stdout=json.dumps({"cash_max_qty": "10"}))
        try:
            rc, out, _ = run_cli("max-qty", "TSLA.US", "--side", "buy", "--order-type", "MO", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["order_type"], "MO")
        finally:
            os.unlink(bp)

    def test_portfolio_combo(self):
        bp = make_fake(branches={
            "positions": json.dumps([]),
            "fund-positions": json.dumps([]),
            "balance": json.dumps([{"currency": "USD", "total_cash": "1000"}]),
        })
        try:
            rc, out, _ = run_cli("portfolio", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertIn("positions", out["datas"])
            self.assertIn("fund_positions", out["datas"])
            self.assertIn("balance", out["datas"])
        finally:
            os.unlink(bp)


if __name__ == "__main__":
    unittest.main()
