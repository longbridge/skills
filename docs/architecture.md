# Skill 设计:多语言 + 工具选择

本仓库的两个核心设计决定 — **三语支持** 和 **CLI vs MCP 路径选择** — 都不是写在代码里的运行时分支,而是写成 SKILL.md 里的指令,**让 LLM 在调用时自己决策**。这份文档解释这两套机制怎么工作,以便后续维护者在新增 / 改写 skill 时保持一致。

> 跨文档参考: [Agent Skills 规约](https://agentskills.io/specification) · [microsoft/skills 范式](https://github.com/microsoft/skills) · 本仓库 [README.md](../README.md)

---

## 一、多语言(简体 / 繁體 / English)

### 设计目标

中港台用户都用我们的 skill。要支持:
- 用户用任意一种语言提问 — *"NVDA 现在多少钱"* / *"NVDA 現在多少錢"* / *"What's NVDA's price?"* — LLM 都能正确路由到 `longbridge-quote`
- 回答用**用户的输入语言**,而不是硬编码某一种
- 字段术语 / 错误话术能跟着语言走

**不做**:不用 i18n 框架、不用代码做语言检测、不为每种语言单独维护 SKILL.md。**全部用 prompt 实现,代码层零成本**。

### 实现:四层落点

#### 1️⃣ Description 三语 trigger 关键词 — 决定 **是否激活**

每个 SKILL.md 的 `description` 把同一个语义概念用三种语言写多份关键词。例 [longbridge-quote/SKILL.md](../skills/longbridge-quote/SKILL.md):

```yaml
description: |
  Real-time quotes, static reference, and valuation indices for stocks listed in HK / US / A-share / Singapore via Longbridge Securities. ... Triggers: "现在多少钱", "股价", "涨跌幅", "成交量", "市值", "市盈率", "PE", "PB", "换手率", "行业", "現在多少", "股價", "成交量", "市值", "市盈率", "stock price", "current price", "quote", "market cap", "PE ratio", "valuation", "NVDA price", "AAPL quote", "茅台市值", "腾讯股价", "700.HK", "600519.SH".
```

启动时 agent 只加载 frontmatter(~100 token / skill,这是 [progressive disclosure](https://agentskills.io/specification#progressive-disclosure) 第 1 步)。LLM 用这一行的关键词跟用户问句做模式匹配 — 简体、繁体、英文、ticker 例子任一命中都会触发。

> **要点**:同字的关键词不需要重复(*"成交量"* / *"市值"* 简繁同形,只写一次)。**简繁分歧字**才要写两份(*"现在多少钱"* / *"現在多少錢"*、*"股价"* / *"股價"*)。

#### 2️⃣ Body 顶部的 Response language 指令 — 决定 **输出用什么语言**

每个 SKILL.md 在 `# <skill-name>` 标题之下、第一段 intro 之后,固定一句:

```markdown
> **Response language**: match the user's input language —
> Simplified Chinese / Traditional Chinese / English.
```

这一句的作用是**让 LLM 检测用户输入语言**(简体 / 繁体 / 英文),然后**用同一种语言组织回答**。LLM 多模态语言模型本身就具备这个能力,我们只需在 SKILL 里明确把这条规则提示出来。

`scripts/cli.py` 完全不感知语言 — 它只负责返回 JSON 数据(`success / source / skill / skill_version / datas / error_kind / error / details`)。语言切换发生在 LLM 把 JSON 翻译为自然语言那一步。

#### 3️⃣ 字段对照表 — 数据 → 自然语言时的三语原料

财报 / 估值数据底层是英文字段。SKILL.md(或下沉到 `references/`)给出三列对照表,LLM 按用户语言挑列。例 [longbridge-fundamental/references/field-dictionary.md](../skills/longbridge-fundamental/references/field-dictionary.md):

```markdown
| MCP field            | 简体           | 繁體           | English         |
|---|---|---|---|
| `revenue` / `total_revenue` | 营业收入 / 营收 | 營業收入 / 營收 | Revenue        |
| `cost_of_revenue`    | 营业成本       | 營業成本       | Cost of revenue |
| `gross_margin`       | 毛利率         | 毛利率         | Gross margin   |
| `roe`                | 净资产收益率   | 淨資產收益率   | Return on equity |
```

LLM 渲染回答时,会按 §2 的检测结果挑出对应的列写到响应里。

#### 4️⃣ 错误回复表 — 三语并列

每个 read-tier skill 的 `## Error handling` 章节也是三列,例 [longbridge-quote/SKILL.md](../skills/longbridge-quote/SKILL.md):

```markdown
| `error_kind` | What happened | Reply phrase (zh-Hans / zh-Hant / en) |
|---|---|---|
| `binary_not_found` | longbridge CLI not installed | "长桥 CLI 未安装,请先安装 longbridge-terminal" / "長橋 CLI 未安裝,請先安裝 longbridge-terminal" / "Longbridge CLI not installed: https://github.com/longportapp/longbridge-terminal" |
| `auth_expired` | OAuth token expired | "长桥登录态过期,请跑 `longbridge login`" / "登入過期,請執行 `longbridge login`" / "Login expired — run `longbridge login`." |
```

`cli.py` 永远只返回稳定的 `error_kind` 枚举(`binary_not_found / auth_expired / subprocess_failed / no_input / invalid_input_format / empty_result / risk_block`,共 7 种)+ 内部 `error` 中文话术。LLM 拿到 `error_kind` 之后,在 §4 的表里查对应语言列念给用户听。

### 综合流程

```
                     用户:"NVDA 現在股價"
                            ↓
                  [Claude Code / agent 启动]
   1. 加载所有 SKILL.md frontmatter(~100 token/skill)
                            ↓
              LLM 在 description triggers 中模式匹配
              "現在股價" 命中 longbridge-quote 的 zh-Hant trigger
                            ↓
                  [激活 longbridge-quote SKILL.md]
   2. 读取完整 SKILL.md(英文 body + 三语规则原料)
   3. Response language 指令告诉 LLM:用户用了 zh-Hant → 用 zh-Hant 回答
                            ↓
              python3 scripts/cli.py -s NVDA.US
                            ↓
              cli.py 返回 JSON(英文字段 + 标准 error_kind)
                            ↓
   4. LLM 用 zh-Hant + §3/§4 三语原料生成最终回答:
   "NVDA 現在 209.27 美元,當日下跌 -2.86%。數據來源:長橋證券。"
```

**整套机制完全在 prompt 层。** `cli.py` 不需要任何 i18n 代码;新增一种语言(比如日文 / 韩文 / 西班牙文)= 给 description 加 trigger + 把表加一列,**不用碰 Python**。

---

## 二、CLI vs MCP 工具选择

### 设计目标

每个能力(查行情、查持仓、查资金流……)有两条访问路径:

| 路径 | 接口 | 延迟 | 依赖 |
|---|---|:---:|---|
| **本地 CLI** | subprocess 调 `longbridge` 二进制 | 快(本机进程,~50ms) | 用户本机装了 longbridge-terminal + `longbridge login` |
| **官方 MCP** | HTTP + OAuth(Anthropic MCP transport) | 慢(网络 + 鉴权,~500ms+) | 用户跑过 `claude mcp add longbridge ...` |

每个 SKILL.md 都给 LLM 写明白:**默认 CLI,有条件回退 MCP**。

### 默认规则(读取层 12 个 skill)

```
1. LLM 默认调 python3 scripts/cli.py
2. cli.py 用 shutil.which("longbridge") 找二进制
3. 找不到 → JSON 返回 error_kind=binary_not_found
4. LLM 检测到 binary_not_found → 改调 mcp__longbridge__<等效工具>
5. 用户连 MCP 也没配 → 提示:装 longbridge-terminal 或 claude mcp add
```

每个 read-tier SKILL.md 末尾都有 `## MCP fallback` 章节列出**子命令 ↔ MCP 工具**对照表,例 [longbridge-quote/SKILL.md](../skills/longbridge-quote/SKILL.md):

```markdown
| CLI behaviour | MCP tool |
|---|---|
| `quote` subprocess | `mcp__longbridge__quote` |
| `static` subprocess | `mcp__longbridge__static_info` |
| `calc-index` subprocess | `mcp__longbridge__calc_indexes` |
```

### 4 类例外(SKILL.md 显式覆盖默认)

| 例外 | 默认改成 | 原因 | 写在哪 |
|---|---|---|---|
| **`longbridge-security-list securities`** | **优先 MCP** | 底层 longbridge CLI 当前版本对 security-list 偶发 `param_error`,MCP 走 SDK 直连绕过 CLI 中间层 | [security-list/SKILL.md `## Path-selection note`](../skills/longbridge-security-list/SKILL.md) |
| **`longbridge-subscriptions`** | **CLI 唯一** | MCP 是无状态 HTTP,**没有 WebSocket 会话概念**,无等效工具 | [subscriptions/SKILL.md `## Local-only`](../skills/longbridge-subscriptions/SKILL.md) |
| **分析层 5 个**(valuation / fundamental / news / peer-comparison / portfolio) | **MCP 唯一** | 这些是 `prompt-only` skill,**没有 cli.py**;`requires_mcp: true` 写在 frontmatter 里;调的是纯 MCP 才有的工具(`valuation_history` / `profit_analysis` / `news` / `topic` 等,CLI 全无对应子命令) | 各 analysis-tier SKILL.md `## Prerequisite` |
| **`longbridge-watchlist-admin` dry-run** | **CLI 必须** | dry-run 是 SKILL 层确认机制 — MCP 写工具没有 dry-run 概念。混合走法:dry-run 走 cli.py(不带 `--confirm`),用户确认后,confirm 步骤可走 cli.py(`--confirm`)或 MCP 写工具 | [watchlist-admin/SKILL.md `## Two-step protocol`](../skills/longbridge-watchlist-admin/SKILL.md) |

### 决策流程图

```
                  收到用户问句
                       ↓
  ┌─ 是分析层 skill?(valuation / fundamental / news / peer / portfolio)
  │    └─ 是 ──→ MCP 唯一(没有 cli.py 可走)
  │            └─ MCP 没配?── 提示用户 claude mcp add longbridge ...
  │    └─ 否 ──→ 继续往下
  ↓
  ┌─ 是 mutating skill?(watchlist-admin)
  │    └─ 是 ──→ ① dry-run 必须 cli.py(--no-confirm)
  │              ② LLM 朗读 plan + 等用户回 "确认 / yes / 是的 / confirm"
  │              ③ 用户已确认 → cli.py --confirm 或 MCP 写工具
  │    └─ 否 ──→ 继续往下
  ↓
  ┌─ skill 是否声明优先 MCP?(security-list securities)
  │    └─ 是 ──→ 直接走 MCP
  │    └─ 否 ──→ 默认 cli.py
  ↓
  cli.py 调用
       ├─ exit 0,success: true ──→ 用 cli.py 结果
       ├─ error_kind=binary_not_found ──→ 检 MCP:配了→走 MCP;没配→提示装 CLI
       ├─ error_kind=auth_expired ──→ 提示 longbridge login(MCP 同 OAuth,改不了)
       └─ error_kind=其它 ──→ 按 §错误回复表给用户(不要重试)
```

### CLI / MCP 各自能干什么

| 维度 | CLI(`longbridge` 二进制) | MCP(`mcp__longbridge__*`) |
|---|---|---|
| 行情 / K 线 / 盘口 / 资金流 / 期权 / 窝轮 | ✅ 全部覆盖 | ✅ 全部覆盖 |
| 持仓 / 订单 / 余额 | ✅ 全部覆盖 | ✅ 全部覆盖 |
| 自选股(读) | ✅ | ✅ |
| 自选股(写) | ✅(带 dry-run + confirm gate) | ✅(裸写,需 SKILL 层配 dry-run) |
| **市场情绪历史时序** | ❌ | ✅ `history_market_temperature` |
| **财经日历**(财报 / 分红 / IPO / 宏观) | ❌ | ✅ `finance_calendar` |
| **空头持仓** | ❌ | ✅ `short_positions` |
| **期权成交量分析** | ❌ | ✅ `option_volume / option_volume_daily` |
| **估值历史 + 行业估值分布** | ❌ | ✅ `valuation_history` / `industry_valuation_dist` |
| **完整财报 IS/BS/CF + 一致预期** | ❌ | ✅ `financial_report` / `forecast_eps` / `consensus` |
| **组合 P&L 分析** | ❌ | ✅ `profit_analysis` / `profit_analysis_detail` |
| **新闻 + 公告 + 社区话题** | ❌ | ✅ `news / filings / topic / topic_detail / topic_replies` |
| **券商分享清单** | ❌ | ✅ `sharelist_*`(8 个工具) |
| **WebSocket 实时订阅诊断** | ✅ | ❌(MCP 无状态) |
| **账单 / 报表导出** | ❌ | ✅ `statement_*` |

> **观察**:**分析层 5 个 skill 之所以 MCP-only,正是因为它们依赖的工具(估值历史、财报三表、新闻、组合 P&L)CLI 完全没有对应能力。** 不是设计偏好,是底层能力差异。

### 为什么默认 CLI 而不是默认 MCP?

| 维度 | CLI | MCP |
|---|---|---|
| **延迟** | 本机 subprocess,~50ms | HTTP + OAuth,~500ms+ |
| **网络** | 不需要(已 `longbridge login` 缓存 token) | 必须有公网到 `openapi.longbridge.com` |
| **会话状态** | CLI 持有 WebSocket 长连接,推送 / 订阅可用 | 无状态 HTTP |
| **OAuth scope** | 用户本机 `longbridge login` 时定 | 用户在 `claude mcp add` 后浏览器授权时定(可重新勾选 trade scope) |
| **跨 skill 一致性** | CLI 包了一层,所有 cli.py 共享同一套 envelope + error_kind 规约 | MCP 工具回什么是 longbridge MCP server 决定的,各工具不一定齐 |

简而言之:**只要本机有 CLI,CLI 比 MCP 又快又一致。** MCP 是"加宽能力"(分析 / 历史 / 异步话题)和"兜底"(没装 CLI 时还能跑)用的。

### `error_kind` 是 CLI / MCP 路径选择的胶水

`cli.py` 把所有失败统一收敛成 7 种 `error_kind`:

| `error_kind` | LLM 应对 |
|---|---|
| `binary_not_found` | **路径切换信号** — 改走 MCP |
| `auth_expired` | 提示 `longbridge login`(CLI 和 MCP 共用 OAuth,scope 改不了) |
| `subprocess_failed` | 不重试,把 stderr 给用户 |
| `no_input` / `invalid_input_format` | 业务校验失败,反问用户 |
| `empty_result` | 业务正常的"空"(部分 skill 视作错,见各 SKILL.md) |
| `risk_block` | 仅 mutating skill,binary lock 等安全 gate |

**`binary_not_found` 是路径切换的唯一信号。** 其它 `error_kind` 不应让 LLM 切到 MCP — 因为根本错误不在路径。

---

## 三、维护者指南

新增 / 改写 skill 时,请遵守以下:

1. **三语 trigger 必填** — description 至少覆盖 简 + 繁 + 英 三种关键词。简繁同形可只写一次,分歧字必须分开。
2. **Response language 指令固定写法** — 引用 quote / kline 等已实施的 SKILL.md 直接照抄。不要自己改写措辞,保持跨 skill 一致。
3. **字段表 / 错误表用三列对照** — 不写"中英对照",必须 3 列。
4. **路径规则按本文档分类落 SKILL.md**:
   - 默认读取层 → `## CLI` + `## MCP fallback`
   - 优先 MCP → 加 `## Path-selection note` 说明原因
   - CLI-only → 加 `## Local-only` 说明 MCP 为什么没等效工具
   - MCP-only(分析层) → frontmatter `requires_mcp: true` + `## Prerequisite` 注明 `claude mcp add longbridge ...`
   - mutating → 加 `## Two-step protocol (mandatory)` 写明 dry-run + confirm 流程
5. **`cli.py` envelope 必填字段不能省**:`success / source: "longbridge" / skill / skill_version / datas`(成功)或 `success: false / error_kind / error / details`(失败)。`error_kind` 只能是 7 种枚举之一。
6. **`error_kind=binary_not_found` 是路径切换信号** — `cli.py` 在 `shutil.which()` 返回 None 时必须返回这个,LLM 才能正确地切到 MCP。

---

**最后一条**:这两套机制(三语 + CLI/MCP)的本质都是 — **用 prompt 表达策略,把决策推给 LLM 而不是写运行时代码**。这让单 skill 的 Python 代码极简(几百行的 cli.py + 标准库),增加新策略不用改 Python,而且策略本身可读可审计(直接看 SKILL.md 就懂)。
