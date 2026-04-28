"""Black-box tests for 自选股管理(写) cli.py.

NOTE: No real-account smoke tests — would create test groups in user's account.
"""

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

    def test_create_no_name(self):
        rc, out, _ = run_cli("create-group")
        self.assertEqual(out["error_kind"], "no_input")

    def test_update_no_id(self):
        rc, out, _ = run_cli("update-group")
        self.assertEqual(out["error_kind"], "no_input")

    def test_update_no_changes(self):
        rc, out, _ = run_cli("update-group", "12345")
        self.assertEqual(out["error_kind"], "no_input")

    def test_delete_no_id(self):
        rc, out, _ = run_cli("delete-group")
        self.assertEqual(out["error_kind"], "no_input")


class TestValidation(unittest.TestCase):
    def test_invalid_mode(self):
        rc, out, _ = run_cli("update-group", "12345", "--add", "NVDA.US", "--mode", "weird")
        self.assertEqual(out["error_kind"], "invalid_input_format")


class TestDryRun(unittest.TestCase):
    """No --confirm = dry-run, no binary lookup."""

    def test_create_dry_run(self):
        rc, out, _ = run_cli("create-group", "Test")
        self.assertEqual(rc, 0)
        self.assertTrue(out["dry_run"])
        self.assertEqual(out["plan"]["action"], "create-group")
        self.assertEqual(out["plan"]["name"], "Test")

    def test_update_dry_run(self):
        rc, out, _ = run_cli("update-group", "12345", "--add", "NVDA.US", "--add", "AAPL.US")
        self.assertEqual(rc, 0)
        self.assertTrue(out["dry_run"])
        self.assertEqual(out["plan"]["add"], ["NVDA.US", "AAPL.US"])

    def test_delete_dry_run_purge(self):
        rc, out, _ = run_cli("delete-group", "12345", "--purge")
        self.assertEqual(rc, 0)
        self.assertTrue(out["dry_run"])
        self.assertTrue(out["plan"]["purge"])


class TestBinaryLockGate(unittest.TestCase):
    """Gate 2: with --confirm, --longbridge-bin must resolve to PATH (not arbitrary path)."""

    def test_confirm_with_arbitrary_path_blocked(self):
        bp = make_fake(stdout=json.dumps({"group_id": "999"}))
        try:
            rc, out, _ = run_cli("create-group", "Test", "--confirm", "--longbridge-bin", bp)
            self.assertEqual(rc, 2)
            self.assertEqual(out["error_kind"], "risk_block")
            self.assertEqual(out["details"]["gate"], "binary_locked")
        finally:
            os.unlink(bp)

    def test_dry_run_with_arbitrary_path_ok(self):
        # Dry-run mode allows fake binary (for testing) since no subprocess call
        bp = make_fake(stdout="")
        try:
            rc, out, _ = run_cli("create-group", "Test", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertTrue(out["dry_run"])
        finally:
            os.unlink(bp)


class TestBinaryNotFound(unittest.TestCase):
    def test_confirm_path_nonexistent(self):
        rc, out, _ = run_cli("create-group", "Test", "--confirm", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        # An arbitrary path that doesn't exist + confirm → risk_block (locked) too
        # because the lock gate also catches this case
        self.assertIn(out["error_kind"], {"risk_block", "binary_not_found"})


if __name__ == "__main__":
    unittest.main()
