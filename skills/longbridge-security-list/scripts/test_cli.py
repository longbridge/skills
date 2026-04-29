"""Black-box tests for 证券查找 cli.py."""

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


class TestMarket(unittest.TestCase):
    def test_invalid_market(self):
        rc, out, _ = run_cli("securities", "--market", "XYZ")
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_sh_alias(self):
        bp = make_fake(stdout=json.dumps([{"symbol": "600000.SH", "name_cn": "X"}]))
        try:
            rc, out, _ = run_cli("securities", "--market", "sh", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["market"], "CN")
        finally:
            os.unlink(bp)


class TestBinary(unittest.TestCase):
    def test_missing(self):
        rc, out, _ = run_cli("securities", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        self.assertEqual(out["error_kind"], "binary_not_found")


class TestSubprocess(unittest.TestCase):
    def test_auth(self):
        bp = make_fake(stderr="please login\n", exit_code=1)
        try:
            _, out, _ = run_cli("securities", "--longbridge-bin", bp)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bp)


class TestSecuritiesHappy(unittest.TestCase):
    def test_securities(self):
        fake = json.dumps([{"symbol": "700.HK", "name_cn": "腾讯", "name_en": "TENCENT"}])
        bp = make_fake(stdout=fake)
        try:
            rc, out, _ = run_cli("securities", "--market", "HK", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["market"], "HK")
            self.assertEqual(out["count"], 1)
        finally:
            os.unlink(bp)


class TestParticipantsHappy(unittest.TestCase):
    def test_participants(self):
        fake = json.dumps([{"broker_id": 1, "name_cn": "汇丰", "name_en": "HSBC"}])
        bp = make_fake(stdout=fake)
        try:
            rc, out, _ = run_cli("participants", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "participants")
            self.assertEqual(len(out["datas"]), 1)
        finally:
            os.unlink(bp)


if __name__ == "__main__":
    unittest.main()
