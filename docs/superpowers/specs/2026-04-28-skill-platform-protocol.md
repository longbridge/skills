# Longbridge Skill 平台规约

**Date:** 2026-04-28
**Status:** Draft (待用户审阅)
**Supersedes:** 部分覆盖 `2026-04-27-longbridge-skill-mvp-design.md`(MVP 那份保留作历史归档,但其中"目录结构 / cli.py 接口 / 错误检测点 / SKILL.md 章节规约"以本文档为准)

## 目的

把 13 个 longbridge skill 共享的工程范式集中沉淀到这一份文档,各个 skill 的设计稿只写"业务差异"部分。改一处改全部,新增 skill 主要是填业务差异表。

适用清单见 `2026-04-28-skill-catalog.md`。

## 目录结构

每个 skill 是一个独立目录(中文名),平铺,不嵌套。

```
<中文名>/
├── SKILL.md           # YAML front-matter + 提示词章节(本文档定义骨架,差异化稿写差异)
├── LICENSE.txt        # Apache-2.0 全文(借鉴 iwencai;所有 skill 同一份,源码层面 symlink)
└── scripts/
    ├── cli.py         # Python 3.8+ 标准库,subprocess 调 longbridge,单文件
    └── test_cli.py    # unittest 黑盒测试(给 skill 维护者用,装到 ~/.claude/skills/ 时不影响)
```

不需要 `references/` `assets/` 这类子目录,除非将来某个 skill 真的需要(比如要带一份大额宏观数据词典)。一旦真要加,在差异化稿里声明,不在本规约里预设。

## SKILL.md 规约

### YAML front-matter(7 个字段)

```yaml
---
name: <中文名>                           # 必填,与目录名一致,做 skill 路由 key
description: <一段三句话>                  # 必填,见下"description 写法"
license: Complete terms in LICENSE.txt    # 必填,固定写这一句
version: 1.0.0                            # 必填,语义化版本,改 SKILL.md 行为时 minor+1,改子进程契约时 major+1
risk_level: read_only | account_read | mutating  # 必填,见下"风险等级"
requires_login: true | false              # 必填,只读市场行情可填 false,涉及账户填 true
default_install: true | false             # 必填,高风险 skill 必须 false
---
```

**description 写法**(决定 LLM 路由):
1. 第一句:能力概括(动词开头,讲查什么/做什么)
2. 第二句:**触发条件**——"当用户询问 / 需要 X、Y、Z 时,**必须**使用此技能"
3. 第三句:覆盖范围 / 限制(支持哪些市场、哪些数据类型)

**风险等级**:
- `read_only`:只读市场公开数据(行情、K 线、盘口等),不需要登录。新会话可放心安装。
- `account_read`:只读账户私有数据(持仓、订单、自选),需要 `longbridge login`。装上不会改账户。
- `mutating`:修改账户状态(下单、撤单、自选股写)。**默认 `default_install: false`**,但 skill 自己的差异化稿里可以基于"操作低风险且可逆"明确论证后改为 `true`(例如自选股管理)。涉及金钱(下单/撤单/改单)的 skill **绝对**不允许 `default_install: true`。

**所有 `mutating` skill 必须有显式 `--confirm` flag + dry-run 流程**,无论 `default_install` 是什么。详细规约写在各自 skill 的差异化稿(参见 #11、#12)。

### 必备章节(9 个)

每个 skill 的 SKILL.md 都必须按此顺序、用相同标题包含这 9 个章节:

1. `## 版本` — 一行,`1.0.0`,与 front-matter 同步
2. `## 技能概述` — 一段话 + 列表,讲清"能查什么、不能查什么、数据来源是长桥证券"
3. `## 何时使用本技能` — 5–8 个典型用户问句,LLM 模式匹配用
4. `## 核心处理流程` — 编号步骤(识别 → 改写参数 → 调用 → 解析 → 回答)
5. `## CLI 接口文档` — argparse 参数表 + 示例 + 退出码
6. `## 输出 JSON Schema` — 默认结构 + 任何变体(差异化稿可在此覆写父文档默认)
7. `## 数据来源标注` — 固定话术见下
8. `## 错误处理` — 把 error_kind 翻成给用户的中文话术
9. `## MCP 备选` — 列出对应官方 MCP 工具(`mcp__longbridge__<tool>`),供 cli.py 不可用时回退
10. `## 代码结构` — 平铺目录树(必须是 skill 实际有的文件)

差异化稿写各章节里要替换/补充的内容,不是把整个 SKILL.md 重写一遍。

## cli.py 接口约定

### 强制约束

- **零依赖**:只用 Python 3.8+ 标准库
- **单文件**:整个 skill 的逻辑只放 `cli.py`,不要拆 `helpers/`
- **stdout 只输出 JSON**:任何日志、调试、warning 都走 stderr
- **shebang**:`#!/usr/bin/env python3`(可执行性可选,推荐)
- **退出码**:`0` 业务成功 / `1` 业务错(empty / 参数错 / 鉴权过期)/ `2` 系统错(找不到二进制 / subprocess 异常)

### 通用 argparse 参数(所有 skill 都有)

| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--format` | enum:`json` | `json` | 占位,目前只支持 json |
| `--longbridge-bin` | path | `longbridge` | 重写底层 CLI 路径,**仅用于测试**;`mutating` skill 禁止接受非 PATH 真实二进制(详见 #11 设计稿) |
| `--timeout` | int seconds | `30` | subprocess 超时 |

各 skill 在差异化稿声明自己的业务参数(如 `--symbol` `--period` 等)。

### JSON envelope schema

**成功**(必备字段):

```json
{
  "success": true,
  "source": "longbridge",
  "skill": "<中文名>",
  "skill_version": "1.0.0",
  "datas": [ /* 业务数据,差异化稿定义形态 */ ]
}
```

差异化稿可以追加同级字段(如 `行情查询` 加 `count` `symbols`,`市场情绪` 加 `market`),但不能改 `success / source / skill / skill_version / datas` 这五个字段的语义。

**失败**(必备字段):

```json
{
  "success": false,
  "source": "longbridge",
  "skill": "<中文名>",
  "skill_version": "1.0.0",
  "error_kind": "<枚举值>",
  "error": "面向 LLM 转述给用户的中文话术",
  "details": { /* 可选,subprocess stderr 摘要、命令行等;不放 stack trace */ }
}
```

### error_kind 枚举(7 种,稳定)

| `error_kind` | 何时触发 | exit | 用户话术(SKILL.md 默认) |
|---|---|---:|---|
| `binary_not_found` | `shutil.which(--longbridge-bin)` 返回 None,或非 PATH 路径不可执行 | 2 | "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal" |
| `auth_expired` | subprocess 退出非 0 且 stderr 含 `login` / `token` / `unauthorized` / `auth`(任一) | 1 | "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权" |
| `subprocess_failed` | subprocess 其它非 0 退出 / TimeoutExpired / OSError | 1 或 2 | "查询失败:<details.stderr>。可以稍后重试或检查参数。" |
| `no_input` | 必填参数为空(symbol、order_id、query 等) | 1 | "请告诉我要查的标的或订单号" |
| `invalid_input_format` | 参数格式不符(symbol 不匹配 `<CODE>.<MARKET>`、日期不是 YYYY-MM-DD 等) | 1 | "格式不对:<details>。<示例>" |
| `empty_result` | subprocess 成功但 datas 为空 | 0(`success: true, datas: []`) **或** 1(若 skill 在差异化稿声明"空结果视为业务错") | "未查到数据,可去 https://longbridge.com 确认" |
| `risk_block` | **仅 `mutating` skill**:超过金额/数量上限、缺少 confirm flag、检测到禁止 mock 二进制时 | 2 | 见 #11 设计稿(每条单独写) |

`empty_result` 默认走"成功 + 空数组"分支(就像 SQL 查询返回 0 行不算错)——只有当 skill 业务上空结果一定是错(比如 `order <id>` 查特定订单查不到)时,在差异化稿声明改成业务错。

### subprocess 调用规范

- 命令模板:`[bin_path, <subcommand>, *args, "--format", "json"]`
- `subprocess.run(..., capture_output=True, text=True, timeout=args.timeout)`
- stderr 关键词识别 `auth_expired`(case-insensitive contains):`login`、`token`、`unauthorized`、`auth`
- stdout 不是合法 JSON → `subprocess_failed`,details 带 `stdout_head: stdout[:500]`
- 多子进程合并(如 `行情查询` 同时调 quote + static):任一失败都中止并返回该错;不做 partial success

### 二进制路径解析(`bin_path` 算法)

```python
def resolve_bin(arg):
    if "/" in arg:
        return arg if (os.path.isfile(arg) and os.access(arg, os.X_OK)) else None
    return shutil.which(arg)
```

`mutating` skill 的 cli.py 在此基础上额外校验:`bin_path` 必须等于 `shutil.which("longbridge")`,不允许传任意路径(防止把测试 fake 二进制接到真账户)。

## test_cli.py 模板

每个 skill 的 `scripts/test_cli.py` 用同一套黑盒模式:

```python
import json, os, subprocess, sys, tempfile, unittest
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
    out = json.loads(proc.stdout) if proc.stdout.strip() else None
    return proc.returncode, out, proc.stderr

def make_fake_longbridge(stdout="", stderr="", exit_code=0, branches=None):
    """Single-payload fake; or pass branches={'quote': '...', 'static': '...'} for multi-subcommand."""
    fd, path = tempfile.mkstemp(prefix="fake-longbridge-", suffix=".py")
    os.close(fd)
    if branches:
        body = "import sys\nsub = sys.argv[1] if len(sys.argv) > 1 else ''\n"
        for k, v in branches.items():
            body += f"if sub == {k!r}: sys.stdout.write({v!r}); sys.exit(0)\n"
        body += f"sys.stderr.write('unknown sub'); sys.exit(1)\n"
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
```

每个 skill 至少要有的测试用例:

1. `test_no_input` — 不传必填参数,断言 `error_kind == "no_input"`、exit 1
2. `test_invalid_input` — 格式错的参数,断言 `error_kind == "invalid_input_format"`、exit 1
3. `test_binary_not_found` — `--longbridge-bin /nonexistent`,断言 `error_kind == "binary_not_found"`、exit 2
4. `test_auth_expired` — fake 二进制 stderr 含 `login`,断言 `error_kind == "auth_expired"`、exit 1
5. `test_subprocess_failed` — fake 二进制非 0 退出且 stderr 不含登录关键词,断言 `error_kind == "subprocess_failed"`
6. **happy path**(每个 skill 至少 1 条) — fake 二进制返回有效 JSON,断言 `success: true` 与差异化稿定义的 `datas` 形态
7. **空结果** — fake 二进制返回 `[]`,断言按差异化稿声明走 success-empty 还是 `empty_result` 分支

`mutating` skill 额外加 risk_block 测试(详见 #11)。

## 数据来源标注

固定话术,所有 skill 在 SKILL.md `## 数据来源标注` 章节复制:

> **重要提示**:
> - 引用本技能返回的任何价格、涨跌、市值、账户、订单数据时,**必须**强调"数据来源于长桥证券"
> - 如果未查到数据,引导用户去 https://longbridge.com 或长桥 App 确认

`mutating` skill 把这段改写为"操作通过长桥证券完成,以长桥 App 内显示为准",见 #11。

## License 与版本

- `LICENSE.txt` 全部 skill 同一份 Apache-2.0 全文。建议在仓库根放一份 `LICENSE.txt`,各 skill 目录用 symlink 指过去(`ln -s ../../LICENSE.txt LICENSE.txt`)。
- `version` 字段语义:
  - patch (`1.0.x`):typo 修复、不影响行为
  - minor (`1.x.0`):新增 cli.py 参数、扩展 datas 字段(向下兼容)
  - major (`x.0.0`):删/改字段、改 error_kind 枚举、改 SKILL.md 触发逻辑

## MCP 与 CLI 的双路模型

每个 skill 默认走本地 `longbridge` CLI(subprocess + 本机 OAuth),但 SKILL.md 必须包含 `## MCP 备选` 章节,列出对应的官方 MCP 工具名(`longbridge-mcp` 项目里 `pub async fn <name>` 直接对应 `mcp__longbridge__<name>`)。

**LLM 路由原则**(写在每个 SKILL.md 里的"步骤 0"):
1. **优先 cli.py**——本机 subprocess 更快、不走网络;
2. **若 cli.py 返回 `binary_not_found`**(本机没装 longbridge CLI),改用 MCP 工具;
3. **若用户问的是 CLI 不支持的能力**(基本面 / 财经日历 / 资讯 / 提醒 / DCA / A/H 溢价 / 经纪商持仓 / 异动 / 指数成分等),直接走 MCP,不用 cli.py。

用户启用 MCP 的方式:

```bash
claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
```

首次工具调用触发浏览器 OAuth(token 缓存,自动刷新)。

`mutating` skill(#11 股票交易、#12 自选股管理)在 MCP 路径上仍要遵守 dry-run + confirm 双步流程——SKILL.md 必须明确"无论走 cli.py 还是 MCP,LLM 第一次调用都不带 confirm,把 plan 朗读给用户后等明确确认"。

## 部署方式

```bash
# 推荐:符号链接,便于本仓库内迭代
mkdir -p ~/.claude/skills
ln -s "$PWD/<中文名>" "$HOME/.claude/skills/longbridge-<英文别名>"
```

`mutating` skill 必须用 symlink 而非 cp -r,以确保仓库内"风险评估稿 + 部署 gate"任何变更都能立即生效到已安装位置。详见 #11 设计稿。

英文别名规则:`longbridge-<功能简写>`,例如 `longbridge-quote / longbridge-kline / longbridge-positions / longbridge-trading`。

## 验收基线(每个 skill 都必过)

1. **单测**:`python3 scripts/test_cli.py` 全绿
2. **真实烟测**:`python3 scripts/cli.py <最少必填参数>` 用真账户跑通,exit 0
3. **错误层**:5 种通用 error_kind 全部能复现并返回正确话术
4. **集成**:`ln -s` 到 `~/.claude/skills/`,新开 Claude Code 会话用 4–6 条该 skill 在 SKILL.md `何时使用` 章节列的样本问句,模型每条都正确路由 + 给出含数据的回答 + 引用长桥证券

第 4 步集成测试结果记到对应差异化稿的 `## 验收日志` 章节。

## 与 iwencai 范式的差异

| 维度 | iwencai SkillHub | 本规约 |
|---|---|---|
| 数据来源 | SaaS 网关 `openapi.iwencai.com` + API Key | 本地 `longbridge` Rust CLI + OAuth |
| 鉴权 | `Authorization: Bearer $IWENCAI_API_KEY` | 底层 CLI 自己管 token,skill 不碰 |
| 调用追踪 | 强制 `X-Claw-*` 自定义 header(skill_id / version / trace_id) | 不需要;subprocess 即追踪 |
| 重试策略 | 失败改写问句最多 2 次 | 不重试;subprocess 失败原样上抛 |
| 部署 | `iwencai-skillhub-cli install <slug>`(zip + 安装器) | 直接 symlink;后续如需安装器再单独设计 |
| Skill 互通 | 共享 query 改写逻辑 | 各 skill 完全独立,共用的只是这份规约 |

## 开放问题(需用户在落地时确认)

1. `LICENSE.txt` 用 Apache-2.0 还是 MIT?(默认 Apache-2.0,与 iwencai 一致)
2. 是否在仓库 root 放共享 `LICENSE.txt` + symlink?(默认是)
3. `mutating` skill 的金额/数量上限默认值放在 `cli.py` 还是 `~/.longbridge/skill-trading.yml`?(详见 #11)
