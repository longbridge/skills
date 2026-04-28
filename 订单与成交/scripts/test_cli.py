"""Black-box tests for 订单与成交 cli.py."""

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


def make_fake(stdout="", stderr="", exit_code=0):
    fd, path = tempfile.mkstemp(prefix="fake-lb-", suffix=".py")
    os.close(fd)
    body = f"import sys\nsys.stdout.write({stdout!r})\nsys.stderr.write({stderr!r})\nsys.exit({exit_code})\n"
    Path(path).write_text("#!/usr/bin/env python3\n" + body)
    os.chmod(path, 0o755)
    return path


class TestNoInput(unittest.TestCase):
    def test_no_subcommand(self):
        rc, out, _ = run_cli()
        self.assertEqual(out["error_kind"], "no_input")

    def test_order_no_id(self):
        rc, out, _ = run_cli("order")
        self.assertEqual(out["error_kind"], "no_input")


class TestValidation(unittest.TestCase):
    def test_invalid_date(self):
        rc, out, _ = run_cli("orders", "--history", "--start", "2024/01/01")
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_invalid_symbol(self):
        rc, out, _ = run_cli("orders", "--symbol", "tsla.us")
        self.assertEqual(out["error_kind"], "invalid_input_format")


class TestBinary(unittest.TestCase):
    def test_missing(self):
        rc, out, _ = run_cli("orders", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        self.assertEqual(out["error_kind"], "binary_not_found")


class TestAuth(unittest.TestCase):
    def test_auth(self):
        bp = make_fake(stderr="please login\n", exit_code=1)
        try:
            _, out, _ = run_cli("orders", "--longbridge-bin", bp)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bp)


class TestHappy(unittest.TestCase):
    def test_orders_today(self):
        bp = make_fake(stdout=json.dumps([{"order_id": "1", "symbol": "TSLA.US"}]))
        try:
            rc, out, _ = run_cli("orders", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["history"], False)
        finally:
            os.unlink(bp)

    def test_orders_history(self):
        bp = make_fake(stdout=json.dumps([]))
        try:
            rc, out, _ = run_cli("orders", "--history", "--start", "2024-01-01", "--end", "2024-12-31", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["history"], True)
            self.assertEqual(out["start"], "2024-01-01")
        finally:
            os.unlink(bp)

    def test_order_detail(self):
        bp = make_fake(stdout=json.dumps({"order_id": "X", "status": "Filled", "quantity": "100"}))
        try:
            rc, out, _ = run_cli("order", "20240101-123", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["order_id"], "20240101-123")
        finally:
            os.unlink(bp)

    def test_order_empty_upgraded_to_business_error(self):
        bp = make_fake(stdout=json.dumps({}))
        try:
            rc, out, _ = run_cli("order", "20240101-nonexistent", "--longbridge-bin", bp)
            self.assertEqual(rc, 1)
            self.assertEqual(out["error_kind"], "empty_result")
        finally:
            os.unlink(bp)

    def test_executions(self):
        bp = make_fake(stdout=json.dumps([{"trade_id": "1"}]))
        try:
            rc, out, _ = run_cli("executions", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "executions")
        finally:
            os.unlink(bp)

    def test_cash_flow(self):
        bp = make_fake(stdout=json.dumps([{"flow_name": "deposit", "balance": "1000"}]))
        try:
            rc, out, _ = run_cli("cash-flow", "--start", "2024-01-01", "--end", "2024-01-31", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "cash-flow")
        finally:
            os.unlink(bp)


if __name__ == "__main__":
    unittest.main()
