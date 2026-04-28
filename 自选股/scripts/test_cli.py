"""Black-box tests for 自选股(只读) cli.py."""

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


SAMPLE = json.dumps([
    {"id": "100", "name": "科技股", "securities": [{"symbol": "NVDA.US"}, {"symbol": "AAPL.US"}]},
    {"id": "200", "name": "港股蓝筹", "securities": [{"symbol": "700.HK"}, {"symbol": "9988.HK"}, {"symbol": "5.HK"}]},
])


class TestBinary(unittest.TestCase):
    def test_missing(self):
        rc, out, _ = run_cli("--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        self.assertEqual(out["error_kind"], "binary_not_found")


class TestAuth(unittest.TestCase):
    def test_auth(self):
        bp = make_fake(stderr="please login\n", exit_code=1)
        try:
            _, out, _ = run_cli("--longbridge-bin", bp)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bp)


class TestHappy(unittest.TestCase):
    def test_no_filter(self):
        bp = make_fake(stdout=SAMPLE)
        try:
            rc, out, _ = run_cli("--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["group_count"], 2)
            self.assertEqual(out["total_symbol_count"], 5)
        finally:
            os.unlink(bp)

    def test_group_id_filter(self):
        bp = make_fake(stdout=SAMPLE)
        try:
            rc, out, _ = run_cli("--group", "100", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["group_count"], 1)
            self.assertEqual(out["datas"][0]["id"], "100")
        finally:
            os.unlink(bp)

    def test_group_name_filter(self):
        bp = make_fake(stdout=SAMPLE)
        try:
            rc, out, _ = run_cli("--group-name", "科技", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["group_count"], 1)
            self.assertIn("科技", out["datas"][0]["name"])
        finally:
            os.unlink(bp)

    def test_filter_no_match(self):
        bp = make_fake(stdout=SAMPLE)
        try:
            rc, out, _ = run_cli("--group", "999", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["group_count"], 0)
            self.assertEqual(out["total_symbol_count"], 0)
        finally:
            os.unlink(bp)


if __name__ == "__main__":
    unittest.main()
