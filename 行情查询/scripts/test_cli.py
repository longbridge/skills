"""Black-box tests for cli.py.

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
    """Run cli.py with given args, return (returncode, stdout_dict, stderr_str)."""
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
    """Single-payload fake; or pass branches={'quote': '...', 'static': '...'} for multi-subcommand."""
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
    def test_no_symbols_returns_business_error(self):
        rc, out, err = run_cli()
        self.assertEqual(rc, 1, f"expected exit 1, got {rc}; stderr={err}")
        self.assertIsNotNone(out, f"stdout was not JSON; stderr={err}")
        self.assertEqual(out.get("success"), False)
        self.assertEqual(out.get("error_kind"), "no_input")
        self.assertEqual(out.get("source"), "longbridge")
        self.assertEqual(out.get("skill"), "行情查询")


class TestSymbolValidation(unittest.TestCase):
    def test_lowercase_symbol_rejected(self):
        rc, out, _ = run_cli("-s", "nvda.US")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_missing_market_suffix_rejected(self):
        rc, out, _ = run_cli("-s", "NVDA")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_unknown_market_rejected(self):
        rc, out, _ = run_cli("-s", "NVDA.XX")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_input_format")


class TestBinaryNotFound(unittest.TestCase):
    def test_missing_binary_returns_system_error(self):
        rc, out, err = run_cli("-s", "NVDA.US", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2, f"expected exit 2, got {rc}; out={out}")
        self.assertEqual(out["error_kind"], "binary_not_found")
        self.assertIn("/nonexistent/longbridge", out.get("details", {}).get("path", ""))


class TestQuoteHappyPath(unittest.TestCase):
    def test_quote_passthrough(self):
        fake_quote = json.dumps([
            {"symbol": "NVDA.US", "last_done": "183.22", "prev_close": "180.25"},
            {"symbol": "700.HK", "last_done": "488.20", "prev_close": "490.00"},
        ])
        bin_path = make_fake_longbridge(stdout=fake_quote)
        try:
            rc, out, err = run_cli("-s", "NVDA.US", "-s", "700.HK", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0, f"stderr={err}")
            self.assertTrue(out["success"])
            self.assertEqual(out["count"], 2)
            self.assertEqual(out["symbols"], ["NVDA.US", "700.HK"])
            self.assertEqual(len(out["datas"]), 2)
            self.assertEqual(out["datas"][0]["symbol"], "NVDA.US")
            self.assertEqual(out["source"], "longbridge")
            self.assertEqual(out["skill"], "行情查询")
            self.assertEqual(out["skill_version"], "1.0.0")
        finally:
            os.unlink(bin_path)


class TestSubprocessErrors(unittest.TestCase):
    def test_auth_expired_detected_from_stderr(self):
        bin_path = make_fake_longbridge(stderr="error: Please run `longbridge login` first.\n", exit_code=1)
        try:
            rc, out, _ = run_cli("-s", "NVDA.US", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 1)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bin_path)

    def test_generic_subprocess_failure(self):
        bin_path = make_fake_longbridge(stderr="error: market closed\n", exit_code=1)
        try:
            rc, out, _ = run_cli("-s", "NVDA.US", "--longbridge-bin", bin_path)
            self.assertEqual(out["error_kind"], "subprocess_failed")
            self.assertIn("market closed", out["details"]["stderr"])
        finally:
            os.unlink(bin_path)


class TestIncludeStaticMerge(unittest.TestCase):
    def test_merges_quote_and_static_by_symbol(self):
        quote = json.dumps([
            {"symbol": "NVDA.US", "last_done": "183.22"},
            {"symbol": "700.HK", "last_done": "488.20"},
        ])
        static = json.dumps([
            {"symbol": "NVDA.US", "name": "NVIDIA Corp", "exchange": "NASDAQ"},
            {"symbol": "700.HK", "name": "TENCENT", "exchange": "HKEX"},
        ])
        bin_path = make_fake_longbridge(branches={"quote": quote, "static": static})
        try:
            rc, out, err = run_cli("-s", "NVDA.US", "-s", "700.HK", "--include-static", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0, f"stderr={err}")
            self.assertTrue(out["success"])
            datas = out["datas"]
            self.assertEqual(len(datas), 2)
            self.assertEqual(datas[0]["symbol"], "NVDA.US")
            self.assertEqual(datas[0]["quote"]["last_done"], "183.22")
            self.assertEqual(datas[0]["static"]["exchange"], "NASDAQ")
            self.assertNotIn("calc_index", datas[0])
        finally:
            os.unlink(bin_path)

    def test_static_missing_for_some_symbols(self):
        quote = json.dumps([
            {"symbol": "NVDA.US", "last_done": "183.22"},
            {"symbol": "OBSCURE.SG", "last_done": "0.50"},
        ])
        static = json.dumps([
            {"symbol": "NVDA.US", "name": "NVIDIA Corp"},
        ])
        bin_path = make_fake_longbridge(branches={"quote": quote, "static": static})
        try:
            rc, out, _ = run_cli("-s", "NVDA.US", "-s", "OBSCURE.SG", "--include-static", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            datas = {d["symbol"]: d for d in out["datas"]}
            self.assertIsNotNone(datas["NVDA.US"]["static"])
            self.assertIsNone(datas["OBSCURE.SG"]["static"])
        finally:
            os.unlink(bin_path)


class TestCalcIndexMerge(unittest.TestCase):
    def test_index_only(self):
        quote = json.dumps([
            {"symbol": "NVDA.US", "last_done": "183.22"},
        ])
        calc = json.dumps([
            {"symbol": "NVDA.US", "pe": "55.4", "pb": "30.1"},
        ])
        bin_path = make_fake_longbridge(branches={"quote": quote, "calc-index": calc})
        try:
            rc, out, err = run_cli("-s", "NVDA.US", "--index", "pe,pb", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0, f"stderr={err}")
            datas = out["datas"]
            self.assertEqual(len(datas), 1)
            self.assertEqual(datas[0]["symbol"], "NVDA.US")
            self.assertEqual(datas[0]["calc_index"]["pe"], "55.4")
            self.assertNotIn("static", datas[0])
        finally:
            os.unlink(bin_path)

    def test_static_and_index_combined(self):
        quote = json.dumps([{"symbol": "NVDA.US", "last_done": "183.22"}])
        static = json.dumps([{"symbol": "NVDA.US", "name": "NVIDIA Corp"}])
        calc = json.dumps([{"symbol": "NVDA.US", "pe": "55.4"}])
        bin_path = make_fake_longbridge(branches={"quote": quote, "static": static, "calc-index": calc})
        try:
            rc, out, _ = run_cli(
                "-s", "NVDA.US",
                "--include-static",
                "--index", "pe",
                "--longbridge-bin", bin_path,
            )
            self.assertEqual(rc, 0)
            data = out["datas"][0]
            self.assertEqual(data["quote"]["last_done"], "183.22")
            self.assertEqual(data["static"]["name"], "NVIDIA Corp")
            self.assertEqual(data["calc_index"]["pe"], "55.4")
        finally:
            os.unlink(bin_path)


if __name__ == "__main__":
    unittest.main()
