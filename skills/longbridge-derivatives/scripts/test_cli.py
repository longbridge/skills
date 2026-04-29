"""Black-box tests for 期权与窝轮 cli.py."""

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

    def test_option_quote_no_contracts(self):
        rc, out, _ = run_cli("option-quote")
        self.assertEqual(out["error_kind"], "no_input")

    def test_option_chain_no_underlying(self):
        rc, out, _ = run_cli("option-chain")
        self.assertEqual(out["error_kind"], "no_input")


class TestUnderlyingValidation(unittest.TestCase):
    def test_warrant_list_non_hk(self):
        rc, out, _ = run_cli("warrant-list", "TSLA.US")
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_invalid_format(self):
        rc, out, _ = run_cli("option-chain", "nvda.US")
        self.assertEqual(out["error_kind"], "invalid_input_format")

    def test_option_chain_invalid_date(self):
        rc, out, _ = run_cli("option-chain", "AAPL.US", "--date", "2024/01/01")
        self.assertEqual(out["error_kind"], "invalid_input_format")


class TestBinaryNotFound(unittest.TestCase):
    def test_missing(self):
        rc, out, _ = run_cli("warrant-issuers", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2)
        self.assertEqual(out["error_kind"], "binary_not_found")


class TestSubprocessErrors(unittest.TestCase):
    def test_auth_expired(self):
        bp = make_fake(stderr="please login\n", exit_code=1)
        try:
            _, out, _ = run_cli("warrant-issuers", "--longbridge-bin", bp)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bp)


class TestOptionQuoteHappy(unittest.TestCase):
    def test_option_quote(self):
        fake = json.dumps([{"symbol": "AAPL250117C190000", "last_done": "5.20", "implied_volatility": "0.32"}])
        bp = make_fake(stdout=fake)
        try:
            rc, out, _ = run_cli("option-quote", "AAPL250117C190000", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["count"], 1)
            self.assertEqual(out["contracts"], ["AAPL250117C190000"])
        finally:
            os.unlink(bp)


class TestOptionChainHappy(unittest.TestCase):
    def test_chain_no_date(self):
        fake = json.dumps({"expiry_dates": ["2025-01-17", "2025-02-21"]})
        bp = make_fake(stdout=fake)
        try:
            rc, out, _ = run_cli("option-chain", "AAPL.US", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertNotIn("date", out)
            self.assertIn("expiry_dates", out["datas"])
        finally:
            os.unlink(bp)

    def test_chain_with_date(self):
        fake = json.dumps([{"strike": "190", "call_symbol": "AAPL250117C190000", "put_symbol": "AAPL250117P190000"}])
        bp = make_fake(stdout=fake)
        try:
            rc, out, _ = run_cli("option-chain", "AAPL.US", "--date", "2025-01-17", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["date"], "2025-01-17")
            self.assertEqual(len(out["datas"]), 1)
        finally:
            os.unlink(bp)


class TestWarrantHappy(unittest.TestCase):
    def test_warrant_list_hk(self):
        fake = json.dumps([{"symbol": "12345.HK", "name": "T123", "leverage_ratio": "3.5"}])
        bp = make_fake(stdout=fake)
        try:
            rc, out, _ = run_cli("warrant-list", "700.HK", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["underlying"], "700.HK")
        finally:
            os.unlink(bp)

    def test_warrant_issuers(self):
        fake = json.dumps([{"issuer_id": 1, "name_cn": "汇丰", "name_en": "HSBC"}])
        bp = make_fake(stdout=fake)
        try:
            rc, out, _ = run_cli("warrant-issuers", "--longbridge-bin", bp)
            self.assertEqual(rc, 0)
            self.assertEqual(out["subcommand"], "warrant-issuers")
        finally:
            os.unlink(bp)


if __name__ == "__main__":
    unittest.main()
