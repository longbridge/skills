"""Black-box tests for 实时订阅 cli.py."""

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


class TestBinary(unittest.TestCase):
    def test_missing(self):
        rc, out, _ = run_cli("--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        self.assertEqual(out["error_kind"], "binary_not_found")


class TestAuth(unittest.TestCase):
    def test_auth_expired(self):
        bp = make_fake(stderr="please login\n", exit_code=1)
        try:
            _, out, _ = run_cli("--longbridge-bin", bp)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bp)


class TestHappy(unittest.TestCase):
    def test_with_subscriptions(self):
        fake = json.dumps([{"symbol": "NVDA.US", "sub_types": ["quote"], "candlestick_periods": []}])
        bp = make_fake(stdout=fake)
        try:
            rc, out, _ = run_cli("--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subscription_count"], 1)
        finally:
            os.unlink(bp)

    def test_empty(self):
        bp = make_fake(stdout=json.dumps([]))
        try:
            rc, out, _ = run_cli("--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subscription_count"], 0)
        finally:
            os.unlink(bp)


if __name__ == "__main__":
    unittest.main()
