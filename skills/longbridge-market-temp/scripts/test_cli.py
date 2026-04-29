"""Black-box tests for 市场情绪 cli.py."""

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


class TestMarketNormalization(unittest.TestCase):
    def test_invalid_market(self):
        rc, out, _ = run_cli("temp", "--market", "XYZ")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_sh_alias_to_cn(self):
        fake = json.dumps({"temperature": "55"})
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, _ = run_cli("temp", "--market", "sh", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertEqual(out["market"], "CN")
        finally:
            os.unlink(bin_path)


class TestHistoryRequiresDates(unittest.TestCase):
    def test_history_no_dates(self):
        rc, out, _ = run_cli("temp", "--history")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_history_invalid_date(self):
        rc, out, _ = run_cli("temp", "--history", "--start", "2024/01/01", "--end", "2024-12-31")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")


class TestBinaryNotFound(unittest.TestCase):
    def test_temp_missing_binary(self):
        rc, out, _ = run_cli("temp", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        self.assertEqual(out["error_kind"], "binary_not_found")


class TestSubprocessErrors(unittest.TestCase):
    def test_auth_expired(self):
        bin_path = make_fake_longbridge(stderr="please login\n", exit_code=1)
        try:
            _, out, _ = run_cli("temp", "--longbridge-bin", bin_path)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bin_path)


class TestTempSnapshotHappy(unittest.TestCase):
    def test_snapshot(self):
        fake = json.dumps({"temperature": "55", "category": "neutral"})
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, _ = run_cli("temp", "--market", "HK", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "temp")
            self.assertEqual(out["market"], "HK")
            self.assertNotIn("start", out)
        finally:
            os.unlink(bin_path)


class TestTempHistoryHappy(unittest.TestCase):
    def test_history(self):
        fake = json.dumps([{"date": "2024-01-01", "temperature": "50"}])
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, _ = run_cli("temp", "--market", "HK", "--history",
                                   "--start", "2024-01-01", "--end", "2024-12-31",
                                   "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertEqual(out["start"], "2024-01-01")
            self.assertEqual(out["end"], "2024-12-31")
        finally:
            os.unlink(bin_path)


class TestSessionHappy(unittest.TestCase):
    def test_session(self):
        fake = json.dumps([{"market": "HK", "begin_time": "09:30", "end_time": "16:00"}])
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, _ = run_cli("session", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "session")
        finally:
            os.unlink(bin_path)


class TestDaysHappy(unittest.TestCase):
    def test_days(self):
        fake = json.dumps({"trading_days": ["2024-01-02"], "half_trading_days": []})
        bin_path = make_fake_longbridge(stdout=fake)
        try:
            rc, out, _ = run_cli("days", "--market", "HK", "--start", "2024-01-01", "--end", "2024-01-05",
                                   "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            self.assertEqual(out["market"], "HK")
            self.assertIn("trading_days", out["datas"])
        finally:
            os.unlink(bin_path)


if __name__ == "__main__":
    unittest.main()
