# Longbridge Skill MVP — 行情查询 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the first Longbridge agent skill `行情查询`, packaged in iwencai SkillHub style (`SKILL.md` + `scripts/cli.py`) and verified end-to-end inside Claude Code.

**Architecture:** A pure-stdlib Python script `cli.py` shells out to the existing Rust binary `longbridge` (subprocess), passes through `--format json`, optionally merges `quote` + `static` outputs by symbol, and emits a stable JSON envelope. `SKILL.md` provides a Chinese prompt directing the LLM to identify symbols, normalize them to `<CODE>.<MARKET>`, invoke `cli.py`, and answer with attribution to 长桥证券.

**Tech Stack:**
- Skill format: Anthropic Agent Skills (`SKILL.md` + `scripts/`)
- cli.py: Python 3.8+ stdlib only (no third-party deps)
- Tests: stdlib `unittest`, black-box via `subprocess` against `cli.py`, with a fake `longbridge` binary written to a tempfile
- Backend: `longbridge` v0.17.4 (Rust) at `~/work/longbridge/longbridge-terminal`, assumed installed and logged in for acceptance steps only

**Spec:** `/Users/hogan/work/longbridge/longbridge-skills/docs/superpowers/specs/2026-04-27-longbridge-skill-mvp-design.md`

---

## File Structure

```
/Users/hogan/work/longbridge/longbridge-skills/
├── .gitignore                              (new) ignore __pycache__, .DS_Store
├── README.md                               (new) project-level pointer
├── docs/superpowers/
│   ├── specs/2026-04-27-longbridge-skill-mvp-design.md   (already exists)
│   └── plans/2026-04-27-longbridge-skill-mvp.md          (this file)
└── 行情查询/
    ├── SKILL.md                            (new) skill prompt + docs
    └── scripts/
        ├── cli.py                          (new) ~150 LOC, stdlib only
        └── test_cli.py                     (new) unittest, black-box
```

**File responsibilities:**

- `行情查询/SKILL.md` — single source of truth for: when LLM should invoke this skill, how to normalize user input, how to call `cli.py`, how to interpret results, how to handle errors. The YAML front-matter `description` field is the load/route signal for Claude Code.
- `行情查询/scripts/cli.py` — argparse → input validation → `subprocess.run(['longbridge', 'quote', ...])` → optional second call for `static` → merge → JSON envelope. Every error path returns a JSON object with `success: false` and an `error_kind` enum.
- `行情查询/scripts/test_cli.py` — invokes `cli.py` as a child process. Uses `tempfile` to write a tiny fake `longbridge` binary (a Python script with shebang) and passes `--longbridge-bin <path>` to control responses. No mocks of internal cli.py functions — all tests are black-box.

**Interface boundaries:**
- `cli.py` is the only module the skill exposes. `test_cli.py` does not import from it.
- Skill consumers (Claude Code, OpenClaw) only read `SKILL.md` and execute `scripts/cli.py`. They never see `test_cli.py` (which lives next to it but is harmless).

---

## Task 1: Bootstrap longbridge-skills repo

**Files:**
- Create: `/Users/hogan/work/longbridge/longbridge-skills/.gitignore`
- Create: `/Users/hogan/work/longbridge/longbridge-skills/README.md`

- [ ] **Step 1: Verify repo state**

Run: `cd /Users/hogan/work/longbridge/longbridge-skills && git status -sb`
Expected: `## No commits yet on master` (or `main`); `docs/` shows as untracked.

- [ ] **Step 2: Write `.gitignore`**

```gitignore
__pycache__/
*.pyc
.DS_Store
.venv/
.pytest_cache/
```

- [ ] **Step 3: Write `README.md`**

```markdown
# Longbridge Skills

Anthropic Agent Skills 风格的长桥能力封装,基于本地 `longbridge` CLI(Rust,见 [longbridge-terminal](../longbridge-terminal))。

每个 skill 都是 `<中文名>/SKILL.md + scripts/cli.py` 的双文件结构,可直接 `cp -r` 到 `~/.claude/skills/` 在 Claude Code 内被自动调用。

## 当前 Skill

- `行情查询/` — 实时报价 + 静态参考(行业/市值/状态),支持港股/美股/A 股/新加坡

## 用法

```bash
# 一次性
cp -r 行情查询 ~/.claude/skills/longbridge-quote
# 或者软链(便于本仓库内迭代)
ln -s "$PWD/行情查询" ~/.claude/skills/longbridge-quote
```

## 前置

- 已安装并登录 `longbridge` CLI:`longbridge login`
- `python3 --version` ≥ 3.8

## 设计/计划文档

- 设计:`docs/superpowers/specs/`
- 实施计划:`docs/superpowers/plans/`
```

- [ ] **Step 4: Verify files**

Run: `ls -la /Users/hogan/work/longbridge/longbridge-skills/{.gitignore,README.md}`
Expected: 两个文件都列出,大小 > 0。

- [ ] **Step 5: Commit**

```bash
cd /Users/hogan/work/longbridge/longbridge-skills
git add .gitignore README.md docs/superpowers/specs/2026-04-27-longbridge-skill-mvp-design.md docs/superpowers/plans/2026-04-27-longbridge-skill-mvp.md
git commit -m "chore: bootstrap longbridge-skills repo with spec + plan"
```

---

## Task 2: Write SKILL.md skeleton + verify structure

**Files:**
- Create: `/Users/hogan/work/longbridge/longbridge-skills/行情查询/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

The full file content (UTF-8, no BOM):

```markdown
---
name: 行情查询
description: 查询股票实时行情和静态参考信息(报价、涨跌、成交量、行业、市值等)。当用户询问股票当前价格、涨跌幅、成交量、所属行业、市值、上市状态等场景必须使用此技能。支持港股(.HK)、美股(.US)、A股(.SH/.SZ)、新加坡(.SG)。
---

# 行情查询 使用指南

## 技能概述

本技能提供长桥证券实时行情查询能力,支持:
- **实时报价**:最新价、开盘/最高/最低、成交量、成交额、涨跌幅、交易状态
- **静态参考**(可选):行业、市值、上市市场、币种等不变信息
- **多市场**:港股 `.HK`、美股 `.US`、A 股 `.SH`/`.SZ`、新加坡 `.SG`
- **批量**:一次查询多个标的

## 何时使用本技能

当用户询问以下问题时,**必须**使用本技能:
- "NVDA 现在多少钱"、"特斯拉股价"
- "AAPL 和 NVDA 哪个涨得多"、"对比一下 700 和 9988 的涨幅"
- "腾讯今天成交量多少"
- "贵州茅台市值多少"、"宁德时代属于什么行业"
- "苹果还在交易吗"、"今天美股开盘了吗"(单只标的)

## 核心处理流程

### 步骤 1:识别用户提到的标的

从用户问句里抽取股票名称或代码。可以是:
- 公司中文名(腾讯、贵州茅台、特斯拉)
- 英文 ticker(NVDA、AAPL、TSLA)
- 数字代码(700、600519、300750)

### 步骤 2:补全为 `<CODE>.<MARKET>` 格式

按以下规则把名字/代码补全:
- 全大写英文字母 + 美国常见 ticker → 加 `.US`(NVDA → `NVDA.US`)
- 4 位数字 → 港股 `.HK`(700 → `700.HK`,9988 → `9988.HK`)
- 6 位数字以 `60` 开头 → 沪市 `.SH`(600519 → `600519.SH`)
- 6 位数字以 `00`/`30` 开头 → 深市 `.SZ`(300750 → `300750.SZ`)
- 中文公司名 → 用你的知识映射到代码再加后缀(腾讯 → `700.HK`,贵州茅台 → `600519.SH`,特斯拉 → `TSLA.US`)
- 无法判断市场 → **必须反问用户确认**,不要瞎猜

### 步骤 3:调用 CLI

基础查询(只取报价):

```bash
python3 scripts/cli.py -s NVDA.US -s 700.HK
```

如果用户问的是市值、行业、上市市场这类静态属性,加 `--include-static`:

```bash
python3 scripts/cli.py -s 600519.SH --include-static
```

### 步骤 4:解析返回的 JSON

返回结构(基础):

```json
{
  "success": true,
  "count": 2,
  "symbols": ["NVDA.US", "700.HK"],
  "datas": [ {"symbol": "NVDA.US", ...}, {"symbol": "700.HK", ...} ]
}
```

`--include-static` 时,`datas[i]` 形态变为:

```json
{ "symbol": "NVDA.US", "quote": {...}, "static": {...} }
```

某条 symbol 查不到时,对应 `quote` 或 `static` 为 `null`,**整体不会失败**;此时要在回答里说明该 symbol 暂未查到。

错误时:

```json
{
  "success": false,
  "error_kind": "auth_expired" | "binary_not_found" | "subprocess_failed" | "no_symbols" | "invalid_symbol_format",
  "error": "面向用户的中文人话错误描述",
  "details": { "..." }
}
```

按 `error_kind` 处理(下面"错误处理"章节)。

### 步骤 5:回答用户

组织语言时:
- **必须强调数据来源于长桥证券**
- 多标的对比时用表格
- 涨跌用 ▲/▼ 或 +/- 加颜色提示(如果环境支持)
- 不要把 JSON 原样塞给用户,翻译成自然语言

## CLI 接口文档

### 命令行参数

| 参数 | 简写 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `--symbol` | `-s` | 是 | — | 股票代码,可重复多次,格式 `<CODE>.<MARKET>` |
| `--include-static` | — | 否 | false | 同时查询静态参考信息 |
| `--format` | — | 否 | `json` | 输出格式,目前仅支持 `json` |
| `--longbridge-bin` | — | 否 | `longbridge` | 重写底层 CLI 路径(测试/调试用) |

### 调用示例

```bash
# 单个标的报价
python3 scripts/cli.py -s NVDA.US

# 多个标的批量
python3 scripts/cli.py -s NVDA.US -s TSLA.US -s 700.HK

# 报价 + 静态参考
python3 scripts/cli.py -s 600519.SH --include-static
```

### 退出码

- `0` — 业务成功(`success: true`)
- `1` — 业务错误(参数错、空结果)
- `2` — 系统错误(找不到 longbridge 二进制、subprocess 异常)

## 数据来源标注

**重要提示**:
- 引用本技能返回的任何价格、涨跌、市值数据时,**必须**强调"数据来源于长桥证券"
- 没查到数据时,引导用户去 https://longbridge.com 或长桥 App 确认

## 错误处理

按 `error_kind` 给用户的话术:

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal" |
| `auth_expired` | "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权" |
| `subprocess_failed` | "查询失败,详细信息:<details.stderr>。可以稍后重试或检查代码格式。" |
| `no_symbols` | "请告诉我要查的股票代码或公司名" |
| `invalid_symbol_format` | "代码格式不对,要写成 `<CODE>.<MARKET>`,例如 `NVDA.US`、`700.HK`、`600519.SH`" |

## 代码结构

```
行情查询/
├── SKILL.md          # 本文件
└── scripts/
    ├── cli.py        # CLI 入口(零依赖,subprocess 调 longbridge)
    └── test_cli.py   # unittest 测试(可选,装 skill 时可删)
```
```

- [ ] **Step 2: Verify required sections present**

Run:
```bash
cd /Users/hogan/work/longbridge/longbridge-skills/行情查询 && \
  for section in "技能概述" "何时使用本技能" "核心处理流程" "CLI 接口文档" "数据来源标注" "错误处理" "代码结构"; do
    grep -q "^## $section" SKILL.md && echo "OK: $section" || echo "MISSING: $section"
  done && \
  grep -q '^name: 行情查询$' SKILL.md && echo "OK: front-matter name" && \
  grep -q '^description: ' SKILL.md && echo "OK: front-matter description"
```

Expected: 7 个 `OK: <section>` + 2 个 `OK: front-matter ...`,无 `MISSING`。

- [ ] **Step 3: Commit**

```bash
cd /Users/hogan/work/longbridge/longbridge-skills
git add 行情查询/SKILL.md
git commit -m "feat(行情查询): add SKILL.md with prompt and section docs"
```

---

## Task 3: cli.py — argparse skeleton + `no_symbols` error (TDD)

**Files:**
- Create: `/Users/hogan/work/longbridge/longbridge-skills/行情查询/scripts/cli.py`
- Create: `/Users/hogan/work/longbridge/longbridge-skills/行情查询/scripts/test_cli.py`

- [ ] **Step 1: Write the failing test**

Create `行情查询/scripts/test_cli.py`:

```python
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


class TestArgparseAndNoSymbols(unittest.TestCase):
    def test_no_symbols_returns_business_error(self):
        rc, out, err = run_cli()
        self.assertEqual(rc, 1, f"expected exit 1, got {rc}; stderr={err}")
        self.assertIsNotNone(out, f"stdout was not JSON; stderr={err}")
        self.assertEqual(out.get("success"), False)
        self.assertEqual(out.get("error_kind"), "no_symbols")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/hogan/work/longbridge/longbridge-skills/行情查询 && python3 scripts/test_cli.py 2>&1 | tail -10`
Expected: ERROR or FAIL (cli.py doesn't exist yet → subprocess returncode 2 with "No such file" stderr, or `out` is None).

- [ ] **Step 3: Write minimal cli.py**

Create `行情查询/scripts/cli.py`:

```python
#!/usr/bin/env python3
"""Longbridge 行情查询 skill — CLI wrapper around `longbridge quote`/`static`."""

import argparse
import json
import sys


ERROR_KINDS = {
    "auth_expired",
    "binary_not_found",
    "subprocess_failed",
    "no_symbols",
    "invalid_symbol_format",
}


def emit(payload, exit_code):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


def emit_error(kind, message, details=None, exit_code=1):
    assert kind in ERROR_KINDS, f"unknown error_kind: {kind}"
    payload = {"success": False, "error_kind": kind, "error": message}
    if details is not None:
        payload["details"] = details
    emit(payload, exit_code)


def build_parser():
    p = argparse.ArgumentParser(description="Longbridge 行情查询")
    p.add_argument("--symbol", "-s", action="append", default=[], help="标的代码,可多次,格式 <CODE>.<MARKET>")
    p.add_argument("--include-static", action="store_true", help="同时查询静态参考信息")
    p.add_argument("--format", default="json", choices=["json"], help="输出格式")
    p.add_argument("--longbridge-bin", default="longbridge", help="底层 CLI 路径,默认 'longbridge'")
    return p


def main():
    args = build_parser().parse_args()
    symbols = [s.strip() for s in args.symbol if s.strip()]
    if not symbols:
        emit_error("no_symbols", "请告诉我要查的股票代码或公司名")
    # TODO: subsequent tasks add validation, subprocess calls, merging
    emit({"success": True, "count": len(symbols), "symbols": symbols, "datas": []}, 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/hogan/work/longbridge/longbridge-skills/行情查询 && python3 scripts/test_cli.py 2>&1 | tail -10`
Expected: `OK` (1 test passing).

- [ ] **Step 5: Commit**

```bash
cd /Users/hogan/work/longbridge/longbridge-skills
git add 行情查询/scripts/cli.py 行情查询/scripts/test_cli.py
git commit -m "feat(行情查询): cli.py skeleton + no_symbols error path"
```

---

## Task 4: Add `invalid_symbol_format` validation

**Files:**
- Modify: `行情查询/scripts/cli.py` (add validation in main)
- Modify: `行情查询/scripts/test_cli.py` (add test)

- [ ] **Step 1: Write the failing test**

Append to `test_cli.py` (inside the existing `TestArgparseAndNoSymbols` class or a new class — use new class for clarity):

```python
class TestSymbolValidation(unittest.TestCase):
    def test_lowercase_symbol_rejected(self):
        rc, out, err = run_cli("-s", "nvda.US")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_symbol_format")

    def test_missing_market_suffix_rejected(self):
        rc, out, err = run_cli("-s", "NVDA")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_symbol_format")

    def test_unknown_market_rejected(self):
        rc, out, err = run_cli("-s", "NVDA.XX")
        self.assertEqual(rc, 1)
        self.assertEqual(out["error_kind"], "invalid_symbol_format")
```

- [ ] **Step 2: Run tests to verify failure**

Run: `cd 行情查询 && python3 scripts/test_cli.py 2>&1 | tail -15`
Expected: 3 failures (`invalid_symbol_format` not triggered yet).

- [ ] **Step 3: Implement validation in cli.py**

Add at the top of `cli.py` (after imports):

```python
import re

SYMBOL_RE = re.compile(r"^[A-Z0-9]+\.(US|HK|SH|SZ|SG)$")
```

Replace the `if not symbols:` block in `main()` with:

```python
    if not symbols:
        emit_error("no_symbols", "请告诉我要查的股票代码或公司名")
    bad = [s for s in symbols if not SYMBOL_RE.match(s)]
    if bad:
        emit_error(
            "invalid_symbol_format",
            f"代码格式不对: {', '.join(bad)}。要写成 <CODE>.<MARKET>,例如 NVDA.US、700.HK、600519.SH",
            details={"invalid": bad},
        )
```

- [ ] **Step 4: Run tests to verify pass**

Run: `cd 行情查询 && python3 scripts/test_cli.py 2>&1 | tail -10`
Expected: `OK` (4 tests passing — 1 from Task 3 + 3 new).

- [ ] **Step 5: Commit**

```bash
git add 行情查询/scripts/cli.py 行情查询/scripts/test_cli.py
git commit -m "feat(行情查询): validate symbol format <CODE>.<MARKET>"
```

---

## Task 5: Add `binary_not_found` check

**Files:**
- Modify: `行情查询/scripts/cli.py`
- Modify: `行情查询/scripts/test_cli.py`

- [ ] **Step 1: Write the failing test**

Append to `test_cli.py`:

```python
class TestBinaryNotFound(unittest.TestCase):
    def test_missing_binary_returns_system_error(self):
        rc, out, err = run_cli("-s", "NVDA.US", "--longbridge-bin", "/nonexistent/longbridge")
        self.assertEqual(rc, 2, f"expected exit 2, got {rc}; out={out}")
        self.assertEqual(out["error_kind"], "binary_not_found")
        self.assertIn("/nonexistent/longbridge", out.get("details", {}).get("path", ""))
```

- [ ] **Step 2: Run to verify failure**

Run: `cd 行情查询 && python3 scripts/test_cli.py 2>&1 | tail -15`
Expected: 1 failure (binary check not implemented).

- [ ] **Step 3: Implement check in cli.py**

Add to imports: `import shutil`.

Replace the final `emit({...success...})` line in `main()` with:

```python
    bin_path = shutil.which(args.longbridge_bin) if "/" not in args.longbridge_bin else (args.longbridge_bin if os.path.isfile(args.longbridge_bin) and os.access(args.longbridge_bin, os.X_OK) else None)
    if not bin_path:
        emit_error(
            "binary_not_found",
            "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal",
            details={"path": args.longbridge_bin},
            exit_code=2,
        )
    # TODO: Task 6 — call longbridge quote
    emit({"success": True, "count": len(symbols), "symbols": symbols, "datas": []}, 0)
```

Add `import os` at top.

- [ ] **Step 4: Run tests**

Run: `cd 行情查询 && python3 scripts/test_cli.py 2>&1 | tail -10`
Expected: `OK` (5 tests passing).

- [ ] **Step 5: Commit**

```bash
git add 行情查询/scripts/cli.py 行情查询/scripts/test_cli.py
git commit -m "feat(行情查询): detect missing longbridge binary"
```

---

## Task 6: Quote happy path via subprocess (with fake binary)

**Files:**
- Modify: `行情查询/scripts/cli.py` — actually call longbridge subprocess
- Modify: `行情查询/scripts/test_cli.py` — add fake-binary helper + happy-path test

- [ ] **Step 1: Write the failing test**

Append to `test_cli.py` (above `if __name__`):

```python
def make_fake_longbridge(stdout_payload, stderr="", exit_code=0):
    """Write a fake `longbridge` binary that prints stdout_payload (str) and exits exit_code."""
    fd, path = tempfile.mkstemp(prefix="fake-longbridge-", suffix=".py")
    os.close(fd)
    Path(path).write_text(
        "#!/usr/bin/env python3\n"
        "import sys\n"
        f"sys.stdout.write({stdout_payload!r})\n"
        f"sys.stderr.write({stderr!r})\n"
        f"sys.exit({exit_code})\n"
    )
    os.chmod(path, 0o755)
    return path


class TestQuoteHappyPath(unittest.TestCase):
    def test_quote_passthrough(self):
        fake_quote = json.dumps([
            {"symbol": "NVDA.US", "last": "183.22", "prev_close": "180.25"},
            {"symbol": "700.HK", "last": "488.20", "prev_close": "490.00"},
        ])
        bin_path = make_fake_longbridge(fake_quote)
        try:
            rc, out, err = run_cli("-s", "NVDA.US", "-s", "700.HK", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0, f"stderr={err}")
            self.assertTrue(out["success"])
            self.assertEqual(out["count"], 2)
            self.assertEqual(out["symbols"], ["NVDA.US", "700.HK"])
            self.assertEqual(len(out["datas"]), 2)
            self.assertEqual(out["datas"][0]["symbol"], "NVDA.US")
        finally:
            os.unlink(bin_path)
```

- [ ] **Step 2: Run to verify failure**

Run: `cd 行情查询 && python3 scripts/test_cli.py 2>&1 | tail -10`
Expected: failure — `out["datas"]` is empty (we still have stub).

- [ ] **Step 3: Implement subprocess call in cli.py**

Add `import subprocess` to imports.

Replace the trailing block in `main()` (the `# TODO: Task 6` part) with:

```python
    quote_data, err = call_longbridge(bin_path, "quote", symbols)
    if err is not None:
        emit_error(err["kind"], err["message"], details=err.get("details"), exit_code=err.get("exit_code", 1))
    emit({
        "success": True,
        "count": len(symbols),
        "symbols": symbols,
        "datas": quote_data,
    }, 0)
```

Add this helper function near the top (after `emit_error`):

```python
def call_longbridge(bin_path, sub, symbols, timeout=30):
    """Run `longbridge <sub> <symbols...> --format json`. Returns (data, error_dict_or_None)."""
    cmd = [bin_path, sub, *symbols, "--format", "json"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, {
            "kind": "subprocess_failed",
            "message": "查询超时(30s),请稍后重试",
            "details": {"cmd": cmd},
            "exit_code": 2,
        }
    except OSError as exc:
        return None, {
            "kind": "subprocess_failed",
            "message": f"无法启动 longbridge: {exc}",
            "details": {"cmd": cmd, "os_error": str(exc)},
            "exit_code": 2,
        }
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        kind = "auth_expired" if any(w in stderr.lower() for w in ("login", "token", "unauthorized", "auth")) else "subprocess_failed"
        msg = (
            "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权"
            if kind == "auth_expired"
            else f"longbridge {sub} 失败:{stderr or '(stderr empty)'}"
        )
        return None, {
            "kind": kind,
            "message": msg,
            "details": {"cmd": cmd, "stderr": stderr, "returncode": proc.returncode},
        }
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError as exc:
        return None, {
            "kind": "subprocess_failed",
            "message": f"longbridge 返回不是合法 JSON: {exc}",
            "details": {"cmd": cmd, "stdout_head": proc.stdout[:500]},
        }
```

- [ ] **Step 4: Run tests**

Run: `cd 行情查询 && python3 scripts/test_cli.py 2>&1 | tail -10`
Expected: `OK` (6 tests passing).

- [ ] **Step 5: Commit**

```bash
git add 行情查询/scripts/cli.py 行情查询/scripts/test_cli.py
git commit -m "feat(行情查询): wire quote subprocess via call_longbridge helper"
```

---

## Task 7: Subprocess error classification (auth_expired vs subprocess_failed)

**Files:**
- Modify: `行情查询/scripts/test_cli.py` — add 2 tests
- (cli.py already implements the classification in Task 6's `call_longbridge`)

- [ ] **Step 1: Write the failing tests**

Append to `test_cli.py`:

```python
class TestSubprocessErrors(unittest.TestCase):
    def test_auth_expired_detected_from_stderr(self):
        bin_path = make_fake_longbridge("", stderr="error: Please run `longbridge login` first.\n", exit_code=1)
        try:
            rc, out, err = run_cli("-s", "NVDA.US", "--longbridge-bin", bin_path)
            self.assertEqual(out["error_kind"], "auth_expired")
        finally:
            os.unlink(bin_path)

    def test_generic_subprocess_failure(self):
        bin_path = make_fake_longbridge("", stderr="error: market closed\n", exit_code=1)
        try:
            rc, out, err = run_cli("-s", "NVDA.US", "--longbridge-bin", bin_path)
            self.assertEqual(out["error_kind"], "subprocess_failed")
            self.assertIn("market closed", out["details"]["stderr"])
        finally:
            os.unlink(bin_path)
```

- [ ] **Step 2: Run to confirm pass(or any failures)**

Run: `cd 行情查询 && python3 scripts/test_cli.py 2>&1 | tail -10`

If implementation from Task 6 is correct, both tests pass immediately. If they fail, **stop and fix `call_longbridge` in cli.py** (don't move on with red tests).

Expected: `OK` (8 tests passing).

- [ ] **Step 3: Commit**

```bash
git add 行情查询/scripts/test_cli.py
git commit -m "test(行情查询): cover auth_expired vs subprocess_failed classification"
```

---

## Task 8: `--include-static` merge logic

**Files:**
- Modify: `行情查询/scripts/cli.py` — add static call + merge by symbol
- Modify: `行情查询/scripts/test_cli.py` — 2 new tests

- [ ] **Step 1: Write the failing tests**

Append to `test_cli.py`:

```python
def make_dual_fake_longbridge(quote_payload, static_payload):
    """Fake binary that branches on argv[1]: 'quote' vs 'static'."""
    fd, path = tempfile.mkstemp(prefix="fake-longbridge-dual-", suffix=".py")
    os.close(fd)
    Path(path).write_text(
        "#!/usr/bin/env python3\n"
        "import sys\n"
        f"sub = sys.argv[1] if len(sys.argv) > 1 else ''\n"
        f"if sub == 'quote':\n"
        f"    sys.stdout.write({quote_payload!r})\n"
        f"elif sub == 'static':\n"
        f"    sys.stdout.write({static_payload!r})\n"
        f"else:\n"
        f"    sys.stderr.write('unknown sub')\n"
        f"    sys.exit(1)\n"
    )
    os.chmod(path, 0o755)
    return path


class TestIncludeStaticMerge(unittest.TestCase):
    def test_merges_quote_and_static_by_symbol(self):
        quote = json.dumps([
            {"symbol": "NVDA.US", "last": "183.22"},
            {"symbol": "700.HK", "last": "488.20"},
        ])
        static = json.dumps([
            {"symbol": "NVDA.US", "name": "NVIDIA Corp", "industry": "Semiconductors"},
            {"symbol": "700.HK", "name": "TENCENT", "industry": "Internet"},
        ])
        bin_path = make_dual_fake_longbridge(quote, static)
        try:
            rc, out, err = run_cli("-s", "NVDA.US", "-s", "700.HK", "--include-static", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0, f"stderr={err}")
            self.assertTrue(out["success"])
            datas = out["datas"]
            self.assertEqual(len(datas), 2)
            self.assertEqual(datas[0]["symbol"], "NVDA.US")
            self.assertEqual(datas[0]["quote"]["last"], "183.22")
            self.assertEqual(datas[0]["static"]["industry"], "Semiconductors")
        finally:
            os.unlink(bin_path)

    def test_static_missing_for_some_symbols(self):
        quote = json.dumps([
            {"symbol": "NVDA.US", "last": "183.22"},
            {"symbol": "OBSCURE.SG", "last": "0.50"},
        ])
        static = json.dumps([
            {"symbol": "NVDA.US", "name": "NVIDIA Corp"},
        ])
        bin_path = make_dual_fake_longbridge(quote, static)
        try:
            rc, out, err = run_cli("-s", "NVDA.US", "-s", "OBSCURE.SG", "--include-static", "--longbridge-bin", bin_path)
            self.assertEqual(rc, 0)
            datas = {d["symbol"]: d for d in out["datas"]}
            self.assertIsNotNone(datas["NVDA.US"]["static"])
            self.assertIsNone(datas["OBSCURE.SG"]["static"])
        finally:
            os.unlink(bin_path)
```

- [ ] **Step 2: Run to verify failure**

Run: `cd 行情查询 && python3 scripts/test_cli.py 2>&1 | tail -15`
Expected: 2 failures — current cli.py ignores `--include-static`.

- [ ] **Step 3: Implement merge in cli.py**

Replace the final block in `main()` (the `quote_data, err = call_longbridge(...)` and emit) with:

```python
    quote_data, err = call_longbridge(bin_path, "quote", symbols)
    if err is not None:
        emit_error(err["kind"], err["message"], details=err.get("details"), exit_code=err.get("exit_code", 1))

    if not args.include_static:
        emit({
            "success": True,
            "count": len(symbols),
            "symbols": symbols,
            "datas": quote_data,
        }, 0)

    static_data, err = call_longbridge(bin_path, "static", symbols)
    if err is not None:
        emit_error(err["kind"], err["message"], details=err.get("details"), exit_code=err.get("exit_code", 1))

    by_symbol_q = {item.get("symbol"): item for item in (quote_data or []) if isinstance(item, dict)}
    by_symbol_s = {item.get("symbol"): item for item in (static_data or []) if isinstance(item, dict)}
    merged = [
        {
            "symbol": sym,
            "quote": by_symbol_q.get(sym),
            "static": by_symbol_s.get(sym),
        }
        for sym in symbols
    ]
    emit({
        "success": True,
        "count": len(symbols),
        "symbols": symbols,
        "datas": merged,
    }, 0)
```

- [ ] **Step 4: Run all tests**

Run: `cd 行情查询 && python3 scripts/test_cli.py 2>&1 | tail -15`
Expected: `OK` (10 tests passing — 8 prior + 2 new).

- [ ] **Step 5: Commit**

```bash
git add 行情查询/scripts/cli.py 行情查询/scripts/test_cli.py
git commit -m "feat(行情查询): --include-static merges quote and static by symbol"
```

---

## Task 9: Real `longbridge` smoke test (acceptance criteria 1–3)

**Files:**
- No code changes; this is a manual verification gate.

**Prerequisites:**
- `longbridge` is on PATH: `which longbridge`
- Logged in: `longbridge login` was run previously and token is valid (or env vars set)

- [ ] **Step 1: Quote-only smoke test**

Run: `cd /Users/hogan/work/longbridge/longbridge-skills/行情查询 && python3 scripts/cli.py -s NVDA.US -s 700.HK`

Expected:
- exit code 0
- stdout valid JSON with `success: true`, `count: 2`, `symbols: ["NVDA.US", "700.HK"]`, `datas` is a non-empty array of two objects each carrying at least `symbol` and a price-like field

If exit 2 with `binary_not_found`: install longbridge first.
If exit 1 with `auth_expired`: run `longbridge login`.

- [ ] **Step 2: With `--include-static`**

Run: `cd 行情查询 && python3 scripts/cli.py -s NVDA.US --include-static`

Expected:
- exit 0; `datas[0]` has both non-null `quote` and non-null `static`
- `static` object contains industry/name/market-related fields

- [ ] **Step 3: Invalid symbol path**

Run: `cd 行情查询 && python3 scripts/cli.py -s NVDA`

Expected: exit 1, `error_kind: "invalid_symbol_format"`.

- [ ] **Step 4: Record smoke test results**

Append a short note to `行情查询/SKILL.md` is **not** needed — but optionally add an acceptance log to `docs/superpowers/plans/2026-04-27-longbridge-skill-mvp.md` (this file) under a new `## Acceptance Log` section, with the date and the actual outputs (truncated). Then:

```bash
git add docs/superpowers/plans/2026-04-27-longbridge-skill-mvp.md
git commit -m "docs(plan): record acceptance results for cli.py smoke tests"
```

---

## Task 10: Install to `~/.claude/skills/` and integration-verify (acceptance criteria 4)

**Files:**
- No file changes in repo. Side effect: symlink at `~/.claude/skills/longbridge-quote/`.

- [ ] **Step 1: Symlink the skill**

```bash
mkdir -p ~/.claude/skills
[ -e ~/.claude/skills/longbridge-quote ] || ln -s /Users/hogan/work/longbridge/longbridge-skills/行情查询 ~/.claude/skills/longbridge-quote
ls -la ~/.claude/skills/longbridge-quote
```

(Symlink is preferred over `cp -r` so iterations on the spec auto-propagate.)

- [ ] **Step 2: Integration test in fresh Claude Code session**

Manually open a new Claude Code session and ask each of these in sequence; verify each:

| 问句 | 期望行为 |
|---|---|
| "NVDA 现在多少钱" | 模型识别 `NVDA.US`,调用 `longbridge-quote` skill,返回当前价 + 数据来源标注 |
| "AAPL 和 NVDA 哪个涨得多" | 一次调用,带 2 个 symbol,对比涨跌幅 |
| "看一下 700.HK 的市值" | 触发 `--include-static`,从 static 提取市值 |
| "茅台股价多少" | LLM 把"茅台"映射到 `600519.SH`,调用成功 |

每条问句的"通过"判定:
- 模型实际触发了本 skill(可在响应里看到)
- 给出含具体价格/字段的答案
- 引用来源里有"长桥证券"

- [ ] **Step 3: Record results**

Update `docs/superpowers/plans/2026-04-27-longbridge-skill-mvp.md` 的 `## Acceptance Log` 节,加入第 4 条(集成测试)的结果。如果第 4 条失败(尤其"茅台"映射),回到 SKILL.md 步骤 2 改写映射规则,再次跑该问句。

- [ ] **Step 4: Final commit**

```bash
cd /Users/hogan/work/longbridge/longbridge-skills
git add docs/superpowers/plans/2026-04-27-longbridge-skill-mvp.md
git commit -m "docs(plan): record Claude Code integration acceptance"
```

---

## Self-Review

**1. Spec coverage** — every spec section maps to ≥1 task:
- 目录结构 (Spec §3) → Task 1 (repo bootstrap) + Task 2 (创建 行情查询/SKILL.md)
- SKILL.md 章节规约 (Spec §SKILL.md 内容规约) → Task 2 step 1 + step 2 验证 7 个章节
- cli.py 接口规约 (Spec §scripts/cli.py 接口规约): argparse → Task 3; symbol 校验 → Task 4; binary 检测 → Task 5; quote 子进程 → Task 6; 错误分类 → Task 6+7; --include-static → Task 8
- 输出 JSON Schema(默认/--include-static/错误)→ Task 6 / 8 / 4-5-6-7
- 错误检测点(5 种 error_kind)→ Task 3-7 全覆盖
- 验收标准 1-3(单元/静态/错误)→ Task 9
- 验收标准 4(集成)→ Task 10
- 风险与 trade-off → Task 10 step 3 兜底("茅台映射"失败时回写 SKILL.md)

**2. Placeholder scan** — 检查模式:
- "TBD"/"TODO" — Task 5 / Task 6 步骤 3 各有一个 inline `# TODO: Task N` 注释,**这是计划设计的临时占位**,会在后续 Task 的代码块中被覆盖。最终代码无 TODO 注释残留。
- 无 "implement later"/"add appropriate ... handling"/"handle edge cases"
- 每个有代码改动的步骤都给出了完整代码块
- 命令均给出 expected output

**3. Type / 命名一致性**:
- `error_kind` 五值 (`auth_expired`/`binary_not_found`/`subprocess_failed`/`no_symbols`/`invalid_symbol_format`)在 cli.py 的 `ERROR_KINDS` 集合、SKILL.md 的"错误处理"表、test_cli.py 的断言中**三处一致**
- `call_longbridge` 函数签名(Task 6 定义)与 Task 8 的两次调用(`"quote"`/`"static"`)一致
- JSON envelope 字段(`success`/`count`/`symbols`/`datas`/`error_kind`/`error`/`details`)在 cli.py 与 SKILL.md 文档一致
- 使用 `args.longbridge_bin`(argparse 自动把 `--longbridge-bin` 转下划线)— 一致

**4. 子进程超时与退出码**:
- 30s 超时(Task 6)→ TimeoutExpired 转 subprocess_failed exit 2 — spec 说"业务错=1,系统错=2",一致
- binary_not_found exit 2 — 一致
- 所有业务错(no_symbols/invalid_symbol_format/auth_expired/subprocess_failed)默认 exit 1 — 一致

**5. 测试覆盖**:
- 5 种 `error_kind` 全部有测试(Task 3 / 4 / 5 / 7)
- 默认输出 schema(Task 6)、`--include-static` 输出 schema(Task 8)
- 边界:静态部分缺失但 quote 完整(Task 8 second test)
- 总计 10 个 unit test + 4 条手工集成 prompt(Task 10)

---

## Acceptance Log

### 2026-04-28 — 一次性走完 Task 1-10 + Task 11(--index)

**实际实施时按 platform protocol(2026-04-28-skill-platform-protocol.md)做了以下与原 plan 的差异**:
1. SKILL.md front-matter 加了 `version` `risk_level` `requires_login` `default_install` 四个字段
2. JSON envelope 加了 `source` `skill` `skill_version` 三个字段
3. error_kind 重命名:`no_symbols` → `no_input`,`invalid_symbol_format` → `invalid_input_format`(平台规约统一命名)
4. **新增 Task 11**:`--index` 参数 + `calc-index` 子进程 + 三方合并(quote / static / calc-index)。比原 plan 的 10 task 多一份能力,SKILL.md 加了完整 calc-index 字段列表。
5. 新增 `--timeout` 参数(原 plan 硬编码 30s)
6. 总计 12 个 unit test(原 plan 10 个 + calc-index 2 个),全过

### Task 9 — 真账户烟测(2026-04-28)

| 命令 | 结果 |
|---|---|
| `python3 scripts/cli.py -s NVDA.US` | exit 0,NVDA 最新 $216.61 |
| `python3 scripts/cli.py -s NVDA.US -s 700.HK --include-static` | exit 0,两条都含非空 quote + static(NVIDIA / TENCENT,EPS / BPS / dividend_yield 齐全) |
| `python3 scripts/cli.py -s NVDA.US --index pe,pb,turnover_rate` | exit 0,calc_index = `{pe_ttm: 43.84, pb: 33.46, turnover_rate: 0.80}` |
| `python3 scripts/cli.py -s NVDA` | exit 1,error_kind=invalid_input_format |

### Task 10 — Claude Code 集成测试(2026-04-28)

Symlink 部署:`~/.claude/skills/longbridge-quote → /Users/hogan/work/longbridge/longbridge-skills/行情查询`

新会话依次跑了 6 条问句,**全部通过**(模型自动路由到 longbridge-quote skill,返回含数据的回答,引用"长桥证券"):

1. ✅ NVDA 现在多少钱
2. ✅ AAPL 和 NVDA 哪个涨得多
3. ✅ 看一下 700.HK 的市值(触发 --include-static)
4. ✅ 茅台股价多少(LLM 自动映射 茅台 → 600519.SH)
5. ✅ NVDA 现在 PE 多少(触发 --index pe)
6. ✅ 看下 茅台 全貌(同时触发 --include-static + --index)

行情查询 skill #01 全流程关闭。下一步进入 #02 K线查询 / #08 持仓查询 / #10 自选股(只读)。
