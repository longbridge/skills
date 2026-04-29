"""Black-box tests for K线查询 cli.py.

Each test invokes cli.py as a subprocess. A fake `longbridge` binary is
written to a tempfile and passed via --longbridge-bin so tests don't
require the real Rust CLI to be installed.
"""

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
        capture_output=True,
        text=True,
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

    def test_kline_no_symbol(self):
        rc, out, _ = run_cli("kline")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "no_input")

    def test_intraday_no_symbol(self):
        rc, out, _ = run_cli("intraday")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "no_input")


class TestSymbolValidation(unittest.TestCase):
    def test_lowercase_rejected(self):
        rc, out, _ = run_cli("kline", "nvda.US")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_no_market_suffix(self):
        rc, out, _ = run_cli("kline", "NVDA")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_history_missing_start(self):
        rc, out, _ = run_cli("history", "NVDA.US", "--end", "2024-12-31")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_history_missing_end(self):
        rc, out, _ = run_cli("history", "NVDA.US", "--start", "2024-01-01")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_history_invalid_date(self):
        rc, out, _ = run_cli("history", "NVDA.US", "--start", "2024/01/01", "--end", "2024-12-31")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")


class TestBinaryNotFound(unittest.TestCase):
    def test_kline_missing_binary(self):
        rc, out, _ = run_cli("kline", "NVDA.US", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        self.assertEqual(out["error_kind"], "binary_not_found")


class TestSubprocessErrors(unittest.TestCase):
    def test_auth_expired(self):
        bin_path = make_fake_longbridge(stderr="error: Please run `longbridge login` first.\n", exit_code=1)
        try:
            rc, out, _ = run_cli("kline", "NVDA.US", "--longbridge-bin", bin_path)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bin_path)

    def test_generic_failure(self):
        bin_path = make_fake_longbridge(stderr="error: market closed\n", exit_code=1)
        try:
            rc, out, _ = run_cli("kline", "NVDA.US", "--longbridge-bin", bin_path)
            self.assertEqual(out["error_kind"], "subprocess_failed")
        finally:
            os.unlink(bin_path)


class TestKlineHappyPath(unittest.TestCase):
    def test_kline_returns_array(self):
        fake = json.dumps([
            {"time": "2024-01-01 00:00:00", "open": "100", "high": "105", "low": "99", "close": "104", "volume": "1000", "turnover": "100000"},
            {"time": "2024-01-02 00:00:00", "open": "104", "high": "108", "low": "103", "close": "107", "volume": "1200", "turnover": "130000"},
        ])
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, err = run_cli("kline", "NVDA.US", "--period", "day", "--count", "2", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0, f"stderr={err}")
            self.assertTrue(out["success"])
            self.assertEqual(out["subcommand"], "kline")
            self.assertEqual(out["symbol"], "NVDA.US")
            self.assertEqual(len(out["datas"]), 2)
            self.assertEqual(out["skill"], "longbridge-kline")
        finally:
            os.unlink(bin_path)


class TestHistoryHappyPath(unittest.TestCase):
    def test_history_with_dates(self):
        fake = json.dumps([
            {"time": "2024-01-01 00:00:00", "open": "100", "close": "104"},
        ])
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, _ = run_cli("history", "NVDA.US", "--start", "2024-01-01", "--end", "2024-12-31", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "history")
            self.assertEqual(out["start"], "2024-01-01")
            self.assertEqual(out["end"], "2024-12-31")
        finally:
            os.unlink(bin_path)


class TestIntradayHappyPath(unittest.TestCase):
    def test_intraday(self):
        fake = json.dumps([
            {"time": "2024-01-01 09:30:00", "price": "100", "volume": "1000", "turnover": "100000", "avg_price": "100"},
        ])
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, _ = run_cli("intraday", "NVDA.US", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "intraday")
            self.assertEqual(out["symbol"], "NVDA.US")
        finally:
            os.unlink(bin_path)


if __name__ == "__main__":
    unittest.main()
