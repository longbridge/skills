# 安装指南 / Install Guide

## 先决条件 / Prerequisites

不同 tier 的 skill 依赖的底层工具不同 — 按需安装。

### 必装(读取层 12 个 skill)

1. **longbridge CLI**(Rust 二进制,本机进程):

   ```bash
   # macOS / Linux — 详见 https://github.com/longportapp/longbridge-terminal
   brew install longportapp/tap/longbridge          # macOS Homebrew
   # 或下载 release 二进制放 PATH
   ```

   验证:`longbridge --version` 应输出版本号。

2. **登录长桥账户**(OAuth token 缓存到 `~/.longbridge/terminal/.openapi-session`):

   ```bash
   longbridge login
   ```

   浏览器会开授权页;**勾"交易"权限**才能用账户类 skill(`positions / orders / watchlist / watchlist-admin`)。只勾"行情"够用市场只读。

3. **Python 3.8+**(`scripts/cli.py` 用标准库,无第三方依赖):

   ```bash
   python3 --version  # ≥ 3.8
   ```

### 选装(分析层 5 个 skill 必装)

4. **长桥官方 MCP**(分析层 valuation / fundamental / news / peer-comparison / portfolio 完全依赖此项):

   ```bash
   claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
   ```

   首次工具调用触发浏览器 OAuth 授权;`portfolio` 一定要勾"交易"权限,其它 4 个分析 skill 只需"行情"。

   验证:`claude mcp list` 应包含 `longbridge`。

---

## 三种安装方式 / Three install paths

### 方式 A:Claude Code 插件市场(推荐 — 一次装齐 17 个)

#### A1. 远程仓库(已 push 到 GitHub 后)

```bash
# 在 Claude Code 内
/plugin marketplace add longbridge/skills
/plugin install longbridge@longbridge-skills
```

#### A2. 本地路径(开发 / 内测期间)

仓库还没 push 到 GitHub?直接指本地目录:

```bash
# 在 Claude Code 内(替换为你机器上的实际路径)
/plugin marketplace add /Users/hogan/work/longbridge/longbridge-skills
/plugin install longbridge@longbridge-skills
```

> `longbridge` 是插件名(对应 `.claude-plugin/marketplace.json` 里的 `plugins[0].name`);`longbridge-skills` 是 marketplace 名(对应顶层 `name` 字段)。

#### A3. 验证已安装

```bash
/plugin list
# 应能看到 longbridge@longbridge-skills 已 enabled
```

新开 Claude Code 会话后,问一句 *"NVDA 现在多少钱"* 验证 skill 触发。

---

### 方式 B:Symlink 单独 skill 到 `~/.claude/skills/`(挑用)

适合只想装其中几个 skill 而不是全部 17 个。

```bash
mkdir -p ~/.claude/skills

# 行情查询
ln -s /Users/hogan/work/longbridge/longbridge-skills/skills/longbridge-quote \
      ~/.claude/skills/longbridge-quote

# K 线
ln -s /Users/hogan/work/longbridge/longbridge-skills/skills/longbridge-kline \
      ~/.claude/skills/longbridge-kline

# ... 按需复制其它
```

**批量软链全部 17 个**:

```bash
SRC="/Users/hogan/work/longbridge/longbridge-skills/skills"
for d in "$SRC"/*; do
  slug=$(basename "$d")
  ln -sfn "$d" "$HOME/.claude/skills/$slug"
done
ls -la ~/.claude/skills/ | grep longbridge-
```

> **为什么用 symlink 而不是 cp**:仓库本身就是开发版,改 SKILL.md 后立即生效,不用每次都重新部署。生产分发可换成 `cp -R`。

#### ⚠️ 写入类 skill 的特殊安装规约

**`longbridge-watchlist-admin`** 会改用户的自选股状态。批量软链脚本会装它,但它依赖 SKILL.md 里的 dry-run + confirm 双步流程才安全。如果手动审计觉得不放心,可以**先不装它**:

```bash
# 装其它 11 个,跳过 watchlist-admin
SRC="/Users/hogan/work/longbridge/longbridge-skills/skills"
for d in "$SRC"/*; do
  slug=$(basename "$d")
  [[ "$slug" == "longbridge-watchlist-admin" ]] && continue
  ln -sfn "$d" "$HOME/.claude/skills/$slug"
done
```

需要装的时候单独跑 `ln -s`。

---

### 方式 C:其它 agent 产品

skill 文件是纯 Markdown + Python,可直接拷到任何兼容 Agent Skills 规约的 agent。只是默认目录不同:

| Agent 产品 | 默认 skill 目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| OpenCode | `~/.opencode/skills/` |
| Codex(OpenAI) | 见各自文档 |

例(Gemini CLI):

```bash
mkdir -p ~/.gemini/skills
SRC="/Users/hogan/work/longbridge/longbridge-skills/skills"
for d in "$SRC"/*; do
  ln -sfn "$d" "$HOME/.gemini/skills/$(basename $d)"
done
```

> 注意:不同 agent 对 frontmatter 字段的支持度不同(`compatibility` / `allowed-tools` 是实验性的)。本仓库 skill 用的字段都是 spec 规定的标准字段,跨 agent 应该都能识别。

---

## 验证 / Verify

### 1. 仓库自检

在仓库根目录跑:

```bash
python3 scripts/validate-skills.py
```

应输出:

```
Inspected 17 skill(s).
All clean ✓
```

会校验:
- 每个 SKILL.md frontmatter 合规(`name` slug、`description` ≤ 1024 字符)
- `name` 与父目录名严格一致
- 所有读取层 skill 的 `scripts/test_cli.py` 全绿(单测,~1s/skill)

### 2. 真账户烟测(有 longbridge CLI 已登录的话)

```bash
SK="/Users/hogan/work/longbridge/longbridge-skills/skills"

# 行情查询
python3 $SK/longbridge-quote/scripts/cli.py -s NVDA.US

# K 线 5 根日 K
python3 $SK/longbridge-kline/scripts/cli.py kline NVDA.US --period day --count 5

# 自选股
python3 $SK/longbridge-watchlist/scripts/cli.py
```

输出 JSON envelope 的 `success: true` 即成功。

### 3. Claude Code 端到端

新开会话,用以下问句验证(每条覆盖一类 skill):

| 问句 | 应触发 skill |
|---|---|
| *"NVDA 现在多少钱"* | `longbridge-quote` |
| *"特斯拉过去一年走势"* | `longbridge-kline` |
| *"700.HK 盘口"* | `longbridge-depth` |
| *"我的自选股"* | `longbridge-watchlist` |
| *"NVDA 估值贵不贵"* | `longbridge-valuation`(分析层,需 MCP) |

LLM 应在回答里包含 *"数据来源:长桥证券"* / *"Source: Longbridge Securities"* 字样。

---

## 卸载 / Uninstall

### 方式 A 装的(插件市场)

```bash
/plugin uninstall longbridge@longbridge-skills
/plugin marketplace remove longbridge-skills          # 可选,移除市场注册
```

### 方式 B 装的(symlink)

```bash
rm ~/.claude/skills/longbridge-*
# 验证已清理
ls ~/.claude/skills/
```

### 撤销 longbridge CLI 授权

```bash
longbridge logout                                     # 清本机 token
```

### 撤销 longbridge MCP 授权

```bash
claude mcp logout longbridge                          # 撤 OAuth scope
claude mcp remove longbridge                          # 删 MCP 注册
```

---

## 常见问题 / FAQ

### 装好后 skill 没触发

1. 检查 frontmatter triggers 是否覆盖你说的关键词 — 看 [`docs/architecture.md` §1.1](./architecture.md)
2. 检查目录名是否符合 lowercase ASCII slug — 用 `python3 scripts/validate-skills.py` 验
3. Claude Code 启动后才扫 skill,如果是装完后才打开会话不需要重启;但如果 Claude Code 已经在跑,**重启会话**让它重新扫 `~/.claude/skills/`

### `auth_expired` 错

- 读取层市场行情(quote / kline / depth ...)只需 `longbridge login` 时勾**行情**权限
- 账户类(positions / orders / watchlist) **必须勾交易权限** —
  ```bash
  longbridge logout && longbridge login   # 重授,浏览器里勾「交易」
  ```
- MCP 同理:`claude mcp logout longbridge` 后下次任意 MCP 调用重新授权

### `binary_not_found`

cli.py 找不到 `longbridge` 二进制。两种解法:

- **解法 1**(推荐):装 [longbridge-terminal](https://github.com/longportapp/longbridge-terminal)
- **解法 2**:装 MCP(`claude mcp add ...`),让 LLM 自动走 MCP 兜底路径

### `param_error` on `security-list securities`

底层 longbridge CLI 已知 bug。SKILL.md 让 LLM 自动改走 `mcp__longbridge__security_list`,**不需要你手动干预**。

### 分析层 skill 报"this skill has no CLI fallback"

正常 — 分析层 5 个 skill(valuation / fundamental / news / peer-comparison / portfolio)是 prompt-only,**只走 MCP**。先 `claude mcp add longbridge ...` 然后授权交易权限(portfolio 必需,其它 4 个只需行情权限)。

详见 [docs/architecture.md §2 — CLI vs MCP 工具选择](./architecture.md)。
