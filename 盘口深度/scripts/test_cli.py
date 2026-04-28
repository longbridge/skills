"""Black-box tests for 盘口深度 cli.py."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLI = HERE / "cli.py"


def run_cli(*args, env=None):
    proc = subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True, text=True,
        env={**os.environ, **(env or {})},
        timeout=30,
    )
    try:
        out = json.loads(proc.stdout) if proc.stdout.strip() else None
    except json.JSONDecodeError:
        out = None
    return proc.returncode, out, proc.stderr


def make_fake_longbridge(stdout="", stderr="", exit_code=0, branches=None):
    fd, path = tempfile.mkstemp(prefix="fake-longbridge-", suffix=".py")
    os.close(fd)
    if branches:
        body = "import sys\nsub = sys.argv[1] if len(sys.argv) > 1 else ''\n"
        for k, v in branches.items():
            body += f"if sub == {k!r}: sys.stdout.write({v!r}); sys.exit(0)\n"
        body += "sys.stderr.write('unknown sub'); sys.exit(1)\n"
    else:
        body = (
            "import sys\n"
            f"sys.stdout.write({stdout!r})\n"
            f"sys.stderr.write({stderr!r})\n"
            f"sys.exit({exit_code})\n"
        )
    Path(path).write_text("#!/usr/bin/env python3\n" + body)
    os.chmod(path, 0o755)
    return path


class TestNoInput(unittest.TestCase):
    def test_no_subcommand(self):
        rc, out, _ = run_cli()
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "no_input")

    def test_depth_no_symbol(self):
        rc, out, _ = run_cli("depth")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "no_input")


class TestSymbolValidation(unittest.TestCase):
    def test_invalid_symbol(self):
        rc, out, _ = run_cli("depth", "nvda.US")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_brokers_non_hk_rejected(self):
        rc, out, _ = run_cli("brokers", "TSLA.US")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")
        self.assertIn("港股", out["error"])


class TestCountValidation(unittest.TestCase):
    def test_trades_count_zero(self):
        rc, out, _ = run_cli("trades", "700.HK", "--count", "0")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_trades_count_too_large(self):
        rc, out, _ = run_cli("trades", "700.HK", "--count", "1001")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")


class TestBinaryNotFound(unittest.TestCase):
    def test_missing_binary(self):
        rc, out, _ = run_cli("depth", "700.HK", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        self.assertEqual(out["error_kind"], "binary_not_found")


class TestSubprocessErrors(unittest.TestCase):
    def test_auth_expired(self):
        bin_path = make_fake_longbridge(stderr="error: please login\n", exit_code=1)
        try:
            _, out, _ = run_cli("depth", "700.HK", "--longbridge-bin", bin_path)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bin_path)


class TestDepthHappyPath(unittest.TestCase):
    def test_depth(self):
        fake = json.dumps({"asks": [{"price": "100", "volume": "10"}], "bids": [{"price": "99", "volume": "20"}]})
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, _ = run_cli("depth", "700.HK", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertTrue(out["success"])
            self.assertEqual(out["subcommand"], "depth")
            self.assertEqual(out["symbol"], "700.HK")
            self.assertIn("asks", out["datas"])
        finally:
            os.unlink(bin_path)


class TestTradesHappyPath(unittest.TestCase):
    def test_trades(self):
        fake = json.dumps([{"time": "...", "price": "100", "volume": "10", "direction": "Up"}])
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, _ = run_cli("trades", "700.HK", "--count", "5", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertEqual(out["count"], 5)
        finally:
            os.unlink(bin_path)


class TestAllCombo(unittest.TestCase):
    def test_all_hk(self):
        depth = json.dumps({"asks": [], "bids": []})
        brokers = json.dumps({"asks": [], "bids": []})
        trades = json.dumps([])
        bin_path = make_fake_longbridge(branches={"depth": depth, "brokers": brokers, "trades": trades})
        try:
            rc, out, _ = run_cli("all", "700.HK", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "all")
            self.assertIsNotNone(out["datas"]["brokers"])
            self.assertIsNotNone(out["datas"]["depth"])
        finally:
            os.unlink(bin_path)

    def test_all_non_hk_brokers_null(self):
        depth = json.dumps({"asks": [], "bids": []})
        trades = json.dumps([])
        bin_path = make_fake_longbridge(branches={"depth": depth, "trades": trades})
        try:
            rc, out, _ = run_cli("all", "TSLA.US", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertIsNone(out["datas"]["brokers"])
        finally:
            os.unlink(bin_path)


if __name__ == "__main__":
    unittest.main()
