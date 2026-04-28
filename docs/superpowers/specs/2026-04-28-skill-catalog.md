# Longbridge Skill 全景清单

**Date:** 2026-04-28
**Status:** 18 个 skill 全部 design 已写;读取层 12 个已实施,分析层 5 个 prompt-only 待实施
**Decisions(2026-04-28 brainstorm 锁定):**
- 范围:13 个读取层 skill(#01-#13) + 5 个分析层 skill(#14-#18)= 18
- spec 粒度:1 份平台规约 + 18 份短差异化稿
- 交易类(#11):P0 出 design + 部署 gate(`default_install: false`),实施推迟 P2
- 分析层(#14-#18):prompt-only,无 cli.py,**强依赖 MCP**(用户需 `claude mcp add longbridge ...`)
- 目录:全部留 `longbridge-skills/`,部署用 symlink 到 `~/.claude/skills/`

## 调研背景

参考 iwencai SkillHub(`https://www.iwencai.com/skillhub`)的官方 skill 集合(快照存于
`/Users/hogan/work/longbridge/clawdbot-skills/_iwencai-snapshot/`),抽出可借鉴的设计要素,
并结合本地 `longbridge` CLI v0.17.4 的 30+ 子命令,规划长桥版 skill 全景。

### iwencai SkillHub 现状(9 个官方 skill)

| 排序 | name | 中文名 | 下载量 |
|---:|---|---|---:|
| 1 | hithink-market-query | 行情数据查询 | 253 |
| 2 | hithink-zhishu-query | 指数数据查询 | 192 |
| 3 | hithink-sector-selector | 问财选板块 | 168 |
| 4 | hithink-industry-query | 行业数据查询 | 147 |
| 5 | hithink-macro-query | 宏观数据查询 | 116 |
| 6 | hithink-management-query | 公司股东股本查询 | 93 |
| 7 | hithink-insresearch-query | 机构研究与评级查询 | 92 |
| 8 | hithink-usstock-selector | 问财选美股 | 60 |
| 9 | hithink-hkstock-selector | 问财选港股 | 56 |

### iwencai 设计要点(可直接照搬到我们)

- SKILL.md 顶部 `description` 用「**当用户询问 X、Y、Z 时,必须使用此技能**」触发句式
- 「核心处理流程」用编号步骤清楚拆「识别 → 改写 → 调用 → 解析 → 回答」
- 强调**数据来源**(他们说"同花顺问财",我们说"长桥证券")
- 单独一段「错误处理」,把 error_kind 翻成对用户的话术
- `LICENSE.txt` 与 `SKILL.md` 同级,合规
- SKILL.md 里写明 `## 版本` 字段,便于灰度

### iwencai 用了但我们**不需要**的

- 全部 skill 共享一个 HTTP 网关(`https://openapi.iwencai.com/v1/query2data`)+ API Key 鉴权
- 自然语言 query 改写(因为他们的 API 是问句进、表格出)
- 各种 `X-Claw-*` 自定义 header 做调用追踪 / skill 路由
- 失败重试改写问句(最多 2 次)

我们走 subprocess 调本地 `longbridge` CLI,鉴权由底层 OAuth 处理,subcommand 结构本身就替代了 query 改写,不需要这套云网关协议。

---

## 长桥 Skill 全景(13 个)

按"市场只读 / 账户只读 / 个人化 / 交易写入 / 元能力"五大类组织,**完全覆盖 longbridge CLI 的当前能力**。

### A) 市场行情类(7 个,只读,无账户/合规风险)

| # | Skill 名 | longbridge 子命令 | 典型问句 | 说明 |
|---:|---|---|---|---|
| 1 | **行情查询** | `quote` / `static` / `calc-index` | "NVDA 现在多少"、"贵州茅台市值"、"700 PE 是多少" | ★MVP 已设计稿;指数行情(HSI.HK 等)合并进来,不单独再做 |
| 2 | **K线查询** | `kline` / `kline-history` | "茅台过去一年走势"、"NVDA 5 分钟 K"、"今日分时" | 需要 `intraday` 时纳入;支持周/日/分钟多 granularity |
| 3 | **盘口深度** | `depth` / `brokers` / `trades` | "看下 700 的盘口"、"NVDA 逐笔"、"港股经纪商队列" | 5 档行情 + 经纪商 + 逐笔成交,微观结构三件套 |
| 4 | **资金流向** | `capital-flow` / `capital-dist` | "今日主力资金净流入"、"大单分布" | iwencai 把这合并进行情;我们独立成 skill,问句更清晰 |
| 5 | **市场情绪** | `market-temp` / `trading-session` / `trading-days` | "今天美股开盘吗"、"港股温度计"、"下个交易日" | 把"市场是否开市/温度"打包,场景上接近 |
| 6 | **期权与窝轮** | `option-quote` / `option-chain` / `warrant-quote` / `warrant-list` / `warrant-issuers` | "TSLA 下个月期权链"、"700 的牛熊证"、"恒指认购窝轮" | 衍生品独立成 skill,LLM 一看就知道是衍生品语义 |
| 7 | **证券查找** | `security-list` / `participants` | "港股全部股票列表"、"经纪商 ID 9000 是谁" | 元数据/字典,使用频次低但偶尔需要 |

### B) 账户只读类(2 个,需 `longbridge login`,但只读)

| # | Skill 名 | longbridge 子命令 | 典型问句 | 说明 |
|---:|---|---|---|---|
| 8 | **持仓查询** | `positions` / `fund-positions` / `balance` / `margin-ratio` / `max-qty` | "我现在持仓"、"账户余额"、"NVDA 我能买多少股" | ★规划中;账户全景 + 保证金 + 可买量 |
| 9 | **订单与成交** | `orders` / `order` / `executions` / `cash-flow` | "今天的订单"、"上个月所有成交"、"账户出入金记录" | 订单(含历史)+ 成交明细 + 资金流水 |

### C) 个人化(1 个,只读)

| # | Skill 名 | longbridge 子命令 | 典型问句 | 说明 |
|---:|---|---|---|---|
| 10 | **自选股** | `watchlist`(只读:list / show) | "我的自选股"、"自选股里港股涨幅" | ★规划中;增删改放 D 类风险评估后再说 |

### D) 写入/交易类(2 个,**默认不安装**,需用户显式开启)

| # | Skill 名 | longbridge 子命令 | 典型问句 | 说明 |
|---:|---|---|---|---|
| 11 | **股票交易** | `buy` / `sell` / `cancel` / `replace` | "买 100 股 NVDA 限价 180"、"撤单 12345"、"改单 12345 改到 188" | **高风险**:必须 SKILL.md 明确"每次下单必须二次确认",底层 longbridge CLI 已有 confirm prompt 做 belt-and-suspenders;接收 `--longbridge-bin` 时**禁止** mock |
| 12 | **自选股管理** | `watchlist`(create / update / delete) | "把 NVDA 加到自选"、"删除自选分组「科技股」" | 中等风险(只改自选,不动钱);可以单独成 skill,也可以并入 #10 用 flag 区分 |

### E) 元能力(1 个,可选)

| # | Skill 名 | longbridge 子命令 | 说明 |
|---:|---|---|---|
| 13 | **实时订阅** | `subscriptions` | 列出当前 WebSocket 订阅;LLM 用例少,优先级最低 |

---

## 不做的(longbridge CLI 也没有的能力)

iwencai 有但我们没有的能力,**短期不做**(底层不支持):

- 板块筛选(`hithink-sector-selector`)
- 行业估值/排名查询(`hithink-industry-query`)
- 宏观经济指标(`hithink-macro-query`)
- 公司股本/股东(`hithink-management-query`)
- 机构研究/研报评级(`hithink-insresearch-query`)
- 美股/港股筛选器(`hithink-usstock-selector` / `hithink-hkstock-selector`)

如果将来要补,需要先在 longbridge-terminal 加底层接口(可能要走第三方数据源),不是 skill 层能解决的。

---

## 实施优先级(基于 iwencai 下载量 + 长桥账户场景刚需)

### P0(MVP + 第一波,~6 周)

按之前讨论(用户已确认 A+B):MVP 先 1,然后追加 2/8/10,共 4 个 skill。

| 序 | Skill | 依据 |
|---:|---|---|
| 1 | **行情查询** ✅ MVP 已有 spec/plan,先实施 | iwencai 下载量 #1,刚需 |
| 2 | **K线查询** | 行情的天然延伸;iwencai 下载量未单列 K 线但 market-query 中包含 |
| 8 | **持仓查询** | 长桥独家(iwencai 没有),"我账户怎么样"是高频问句 |
| 10 | **自选股**(只读) | 长桥独家;个人化入口,后续可联动 #1/#2 做组合查询 |

### P1(第二波,~4 周)

补齐市场只读类的常用部分:

| 序 | Skill | 依据 |
|---:|---|---|
| 4 | 资金流向 | "主力资金"是中文用户高频问句 |
| 3 | 盘口深度 | 短线/日内场景常用 |
| 9 | 订单与成交 | 配套持仓查询,组成"账户全景" |

### P2(第三波,~6 周)

衍生品 + 元数据 + 风险写入类:

| 序 | Skill | 依据 |
|---:|---|---|
| 6 | 期权与窝轮 | 衍生品有用户群,但语义需精细 |
| 5 | 市场情绪 | 短查询,实现简单,可顺手做 |
| 11 | **股票交易** ⚠️ | **单独 risk review**,confirm 流程必须验证完备才上 |
| 12 | 自选股管理(写) | 可与 #10 合并 |

### P3(可选,优先级最低)

| 序 | Skill | 备注 |
|---:|---|---|
| 7 | 证券查找 | 元数据,LLM 用例少 |
| 13 | 实时订阅 | 推送场景目前不在 skill 用例 |

---

## 与 iwencai 共享的工程范式

不论选哪几个 skill 实施,所有 skill 都按同一范式:

```
<中文名>/
├── SKILL.md       # 触发描述 + 处理流程 + 错误话术 + 数据来源标注
├── LICENSE.txt    # 借鉴 iwencai 加上(目前 MVP spec 没要求,可补)
└── scripts/
    ├── cli.py        # Python 3.8+ 标准库,subprocess 调 longbridge
    └── test_cli.py   # unittest 黑盒测试,带 fake longbridge 二进制
```

输出 JSON envelope 与 error_kind 枚举沿用 MVP spec 已定的那套
(`success/count/symbols/datas` + `auth_expired/binary_not_found/subprocess_failed/no_symbols/invalid_symbol_format`)。

## 设计稿索引

平台规约(所有 skill 共享):

- [`2026-04-28-skill-platform-protocol.md`](./2026-04-28-skill-platform-protocol.md) — 目录结构、SKILL.md 规约、cli.py 接口约定、error_kind 枚举、test 模板、部署方式、MCP + CLI 双路模型

### 读取层(13 份,#01-#13,wraps CLI/MCP 1:N)

| # | Skill | 设计稿 | 优先级 |
|---:|---|---|:---:|
| 01 | 行情查询 | [skill-01-quote-design.md](./2026-04-28-skill-01-quote-design.md)(配套 MVP plan) | P0 ✅ |
| 02 | K线查询 | [skill-02-kline-design.md](./2026-04-28-skill-02-kline-design.md) | P0 ✅ |
| 03 | 盘口深度 | [skill-03-depth-design.md](./2026-04-28-skill-03-depth-design.md) | P1 ✅ |
| 04 | 资金流向 | [skill-04-capital-flow-design.md](./2026-04-28-skill-04-capital-flow-design.md) | P1 ✅ |
| 05 | 市场情绪 | [skill-05-market-temp-design.md](./2026-04-28-skill-05-market-temp-design.md) | P2 ✅ |
| 06 | 期权与窝轮 | [skill-06-derivatives-design.md](./2026-04-28-skill-06-derivatives-design.md) | P2 ✅ |
| 07 | 证券查找 | [skill-07-security-list-design.md](./2026-04-28-skill-07-security-list-design.md) | P3 ✅ |
| 08 | 持仓查询 | [skill-08-positions-design.md](./2026-04-28-skill-08-positions-design.md) | P0 ✅ |
| 09 | 订单与成交 | [skill-09-orders-design.md](./2026-04-28-skill-09-orders-design.md) | P1 ✅ |
| 10 | 自选股(读) | [skill-10-watchlist-design.md](./2026-04-28-skill-10-watchlist-design.md) | P0 ✅ |
| 11 | 股票交易 ⚠️ | [skill-11-trading-risk-design.md](./2026-04-28-skill-11-trading-risk-design.md) | **设计 P0 / 实施 P2** |
| 12 | 自选股管理(写) | [skill-12-watchlist-write-design.md](./2026-04-28-skill-12-watchlist-write-design.md) | P2 ✅ |
| 13 | 实时订阅 | [skill-13-subscriptions-design.md](./2026-04-28-skill-13-subscriptions-design.md) | P3 ✅ |

### 分析层(5 份,#14-#18,prompt-only,**强依赖 MCP**)

prompt-only = 无 cli.py;SKILL.md 直接编排 MCP 工具 + chain 现有 skill。

| # | Skill | 设计稿 | 解锁的高频问句 |
|---:|---|---|---|
| 14 | 估值分析 | [skill-14-valuation-design.md](./2026-04-28-skill-14-valuation-design.md) | "X 估值贵不贵 / 历史百分位" |
| 15 | 基本面分析 | [skill-15-fundamental-design.md](./2026-04-28-skill-15-fundamental-design.md) | "X 业绩怎么样 / 财务健康吗" |
| 16 | 同行对比 | [skill-16-peer-comparison-design.md](./2026-04-28-skill-16-peer-comparison-design.md) | "X 跟 Y 谁更值得买"(2-5 个 symbol) |
| 17 | 投资组合分析 | [skill-17-portfolio-design.md](./2026-04-28-skill-17-portfolio-design.md) | "我账户表现如何 / 哪只股贡献最多" |
| 18 | 资讯舆情 | [skill-18-news-design.md](./2026-04-28-skill-18-news-design.md) | "X 最近新闻 / 公告 / 市场怎么看" |

**分析层共同特征:**
- 不下投资建议(SKILL.md 强制约束 LLM 不输出"建议买/卖"原话)
- 末尾必须"不构成投资建议"
- 分类输出(不直接 dump raw datas)
- 数据来源标注"长桥证券"

## 实施 plan 顺序

### 读取层(✅ 全部已实施,12 个 symlink 在 `~/.claude/skills/`)

1. ✅ 行情查询 / K线查询 / 持仓查询 / 自选股
2. ✅ 盘口深度 / 资金流向 / 订单与成交
3. ✅ 市场情绪 / 期权与窝轮 / 自选股管理(写)
4. ✅ 证券查找 / 实时订阅
5. ⏸️ 股票交易(#11)— design 稿末尾 4 个先决条件未解决,实施推迟

### 分析层(5 个,prompt-only,待实施)

实施 = 写 SKILL.md(没有 cli.py)+ symlink 到 `~/.claude/skills/`。**前提:用户先 `claude mcp add longbridge ...`**。

实施顺序按预期使用频率:

1. 估值分析(#14)— "贵不贵"是最高频投资问句
2. 基本面分析(#15)— "X 怎么样"第二高频
3. 资讯舆情(#18)— 替代 LLM 乱用 WebSearch
4. 同行对比(#16)— 多 symbol 编排,价值高但触发频率中等
5. 投资组合分析(#17)— 需 trade scope token,触发频率最低
