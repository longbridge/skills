# 估值分析(skill #14)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft(analysis-tier,prompt-only,**强依赖 MCP**)
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`,但**有以下偏离**:
- 无 `scripts/cli.py`(本 skill 是 prompt-only,工具编排在 SKILL.md 里完成)
- 无 `scripts/test_cli.py`(无脚本可单测;集成测试由用户在新会话上跑)
- 强依赖 longbridge MCP,无 MCP 时本 skill 不能用(见 `requires_mcp` front-matter 字段)

## 业务范围

回答**"X 这只股票贵不贵 / 估值合理吗"**这一类问题。

- 编排的 MCP 工具:`valuation`、`valuation_history`、`industry_valuation`、`industry_valuation_dist`、`latest_financial_report`
- chain 到的现有 skill:`行情查询`(拿当前 calc-index PE/PB)
- 不做:基于估值给买卖建议(只给数据 + 分位数,结论让用户自己下);不做行业筛选(我们没数据)

## front-matter

```yaml
---
name: 估值分析
description: 综合分析股票的估值水平——当前 PE / PB / EV/EBITDA 位置,在自身历史中的分位数,跟同行业平均/中位数的对比。当用户询问 X 估值贵不贵 / 是不是被低估 / 历史百分位 / 行业溢价折价等场景必须使用此技能。返回数据驱动的对比,不构成投资建议。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
requires_mcp: true
---
```

`requires_mcp: true` 是新字段,本规约后续可补到平台规约。SKILL.md 在「使用前」段告诉用户:必须 `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`。

## 工具编排逻辑

LLM 收到估值类问句后,**并发**(或串行,看 LLM 实现)调以下工具:

| 工具 | 拿什么 | 必需 |
|---|---|---|
| `mcp__longbridge__valuation` | 当前估值快照(PE / PB / EV/EBITDA / PS / etc.) | 是 |
| `mcp__longbridge__valuation_history` | 历史估值时序(供算分位数) | 是 |
| `mcp__longbridge__industry_valuation` | 行业平均 / 中位数估值 | 是 |
| `mcp__longbridge__industry_valuation_dist` | 行业分位数桶,看自己排第几 | 推荐 |
| `mcp__longbridge__latest_financial_report` | 最新财报 EPS / BPS,用于交叉验证 calc-index 数字 | 可选 |
| 行情查询 skill 的 `cli.py -s X --index pe,pb,turnover_rate` | 当前盘中实时 PE/PB(MCP 的 valuation 可能是收盘后才更新,实时盘中时比对当前价用 calc-index 更新)| 可选 |

## SKILL.md 核心步骤(差异化)

### 步骤 1:识别 symbol(同行情查询规则)

### 步骤 2:并发调 4 个工具

```
mcp__longbridge__valuation(symbol=X)
mcp__longbridge__valuation_history(symbol=X, period="3y")  # 至少 1 年,推荐 3 年看长趋势
mcp__longbridge__industry_valuation(symbol=X)
mcp__longbridge__industry_valuation_dist(symbol=X)
```

### 步骤 3:综合计算

LLM 在 datas 上做:

| 计算 | 方法 |
|---|---|
| 历史 PE 分位数 | 当前 PE 在 valuation_history 时间序列里的百分位(用 LLM 自己排序) |
| 历史 PB 分位数 | 同上 |
| 行业相对溢价 | (当前 PE − 行业中位数 PE) / 行业中位数 PE |
| 行业排名 | 用 industry_valuation_dist 看自己在行业的哪个分位桶 |

### 步骤 4:输出综合判断

回答模板(LLM 必须结构化输出):

```
X (代码) 估值快照(数据来源:长桥证券)

当前估值:
- PE (TTM): 25.3
- PB:        4.1
- PS:        6.8

历史维度(过去 3 年):
- PE 在历史 78 分位(偏高)
- PB 在历史 65 分位(中性偏高)

行业维度(同行业 N 家公司):
- PE 行业中位数 18.2 → 当前比行业贵 39%
- 在行业内 PE 分位:第 5 位 / 共 N 位(高估梯队)

综合:从历史 + 行业两个维度看,当前估值偏高(均在 70+ 分位)。

⚠️ 估值高低不等于"不能买"——成长股长期高估值是常态,需要结合业绩增速看。
本数据不构成投资建议。
```

### 步骤 5:必要时 chain 到其它 skill

- 用户接着问"X 业绩怎么样" → 路由到「基本面分析」skill(#15)
- 用户问"X 跟同行 Y、Z 比哪个贵" → 路由到「同行对比」skill(#16)
- 用户问"X 跌到 N 提醒我" → 路由到 raw MCP `mcp__longbridge__alert_add`

## 输出形态约束(SKILL.md 强制)

- **必须**给三个维度:当前快照 + 历史分位 + 行业分位
- **必须**写"数据来源:长桥证券"
- **必须**末尾加"不构成投资建议"
- **不要**给"建议买 / 不建议买"这类话
- **不要**预测未来 PE 走势
- **可以**指出"历史 X 分位 + 行业 X 分位"组合下的常见解读(如"高估梯队"),但要有 hedge

## 验收清单

- [ ] 装好 MCP 后(`claude mcp list` 含 longbridge),问"NVDA 估值贵不贵",LLM 自动调上述 4-5 个 MCP 工具
- [ ] 回答含三维度(快照 / 历史分位 / 行业分位)
- [ ] 末尾有"不构成投资建议"+ "数据来源:长桥证券"
- [ ] 问"我应该买 NVDA 吗",LLM **拒绝直接给买卖结论**,改给数据 + 引导用户自己判断
- [ ] 问"贵州茅台 跟 五粮液 谁更便宜",LLM **必须**改路由到「同行对比」skill(#16),不在本 skill 硬撑

## 已知 trade-off

- 估值数据滞后:`valuation` MCP 可能是 EOD 数据,盘中价用当日 calc-index 矫正(可选)
- 行业划分按 longbridge 自己的分类,不一定符合用户心理预期(如"宁德时代"在新能源 vs 电池 vs 锂电材料)→ SKILL.md 提示 LLM 在行业归属可疑时跟用户确认
- 周期股的估值"反向"(行业谷底时 PE 高反而是底部)→ SKILL.md 提示 LLM 在能源 / 化工 / 钢铁等周期行业**特别注明**这一点,不要机械地按"PE 高 = 贵"
- 港股 / 美股的"行业"覆盖较好,A 股部分细分行业可能数据稀疏 → 此时 industry_valuation 返回稀疏,LLM 要降级回答(只给历史分位,不给行业分位)
