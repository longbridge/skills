# 期权与窝轮(skill #06)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`

## 业务范围

衍生品(期权 + 窝轮)三件套合一:行情、链表、列表、发行商。

| 子命令 | 何时调 |
|---|---|
| `option-quote` | 用户给定 OCC 期权合约符,问当前行情 |
| `option-chain` | 用户问"X 的期权链",列出到期日;给定到期日时列出 strike |
| `warrant-quote` | 用户给定窝轮代码,问行情 |
| `warrant-list` | 用户问"X 的窝轮 / 牛熊证" |
| `warrant-issuers` | 用户问"窝轮发行商",仅 HK |

## front-matter

```yaml
---
name: 期权与窝轮
description: 查询期权合约行情、期权链(到期日 / strike)、港股窝轮行情、窝轮列表与发行商。当用户询问期权、option、call/put、行权价、到期日、IV、希腊字母、窝轮、牛熊证、认购证、认沽证等衍生品场景必须使用此技能。期权支持美股 / 港股,窝轮仅港股。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---
```

## scripts/cli.py 子命令风格

```
python3 cli.py option-quote   <contract> [<contract> ...]
python3 cli.py option-chain   <underlying> [--date YYYY-MM-DD]
python3 cli.py warrant-quote  <warrant> [<warrant> ...]
python3 cli.py warrant-list   <underlying>            # 必须 .HK
python3 cli.py warrant-issuers                        # 仅 HK,无参数
```

| 参数 | 适用 | 默认 | 说明 |
|---|---|---|---|
| `<contract>` | option-quote | — | 1+ 个 OCC 格式期权合约符(`AAPL240119C190000`) |
| `<underlying>` | option-chain / warrant-list | — | 单个标的,`<CODE>.<MARKET>` |
| `--date` | option-chain | — | 给则返回 strike 列表;不给返回全部到期日 |
| `<warrant>` | warrant-quote | — | 1+ 个港股窝轮代码(`12345.HK`) |

## 输出 JSON Schema

**`option-quote`**:

```json
{
  "success": true, ..., "subcommand": "option-quote",
  "count": 2, "contracts": ["AAPL240119C190000", "..."],
  "datas": [ /* 原 option-quote 数组,每条含 last_done, prev_close, IV, delta, strike, expiry, type */ ]
}
```

**`option-chain`** 不带 `--date`(返回到期日列表):

```json
{ "success": true, ..., "subcommand": "option-chain", "underlying": "AAPL.US",
  "datas": { "expiry_dates": [ /* 原数组 */ ] } }
```

带 `--date`(返回 strike 列表):

```json
{ "success": true, ..., "subcommand": "option-chain", "underlying": "AAPL.US", "date": "2025-01-19",
  "datas": [ /* 原数组,每条含 strike, call_symbol, put_symbol */ ] }
```

**`warrant-quote`** / **`warrant-list`** / **`warrant-issuers`** 各自照搬原 longbridge JSON 输出,顶层套 envelope。

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "TSLA 下个月期权链" → option-chain 列到期日
- "AAPL 1 月 19 日的期权" → option-chain --date
- "AAPL240119C190000 现在多少"(给定合约) → option-quote
- "700.HK 的窝轮" / "腾讯牛熊证" → warrant-list
- "12345.HK 现在价格" → warrant-quote
- "港股窝轮发行商有哪些" → warrant-issuers
- "NVDA call IV 多少"(call 通用问句) → option-chain → 用户挑 → option-quote

### 期权合约符识别

OCC 格式:`<TICKER><YYMMDD><C|P><STRIKE×1000,8 位>`。例如:
- `AAPL240119C190000` = AAPL,2024-01-19 到期,Call,strike $190.00

港股期权合约符:`<TICKER>YYMM<C|P><STRIKE>`(简化形式,具体由 longbridge 决定)

LLM 在 SKILL.md 流程里:
1. 用户给完整 OCC 符 → option-quote
2. 用户给 underlying + 到期 + strike + call/put → 先 option-chain --date 拿到对应合约符,再 option-quote
3. 用户只给 underlying + 时间窗 → option-chain(列到期日),返回让用户挑

### 步骤 3 子命令路由

| 用户语义 | 子命令 |
|---|---|
| OCC 期权符直接报价 | option-quote |
| underlying + "期权链 / option chain" | option-chain |
| underlying + 到期日 + "strike 列表" | option-chain --date |
| HK 窝轮代码报价 | warrant-quote |
| underlying + "窝轮 / 牛熊 / 认购证 / 认沽证" | warrant-list |
| "窝轮发行商" | warrant-issuers |
| underlying 非 .HK + warrant 关键词 | LLM 必须告知"窝轮仅港股可查" |

## 验收清单

- [ ] option-quote:用真实合约符跑通,返回 IV / delta / strike
- [ ] option-chain:`AAPL.US` 不带 date 返回 expiry_dates;带 date 返回 strike 数组
- [ ] warrant-quote:HK 窝轮代码跑通
- [ ] warrant-list:`700.HK` 返回非空数组
- [ ] warrant-list 非 HK 拒绝:`TSLA.US` → `invalid_input_format`
- [ ] warrant-issuers:返回 issuer 列表
- [ ] 集成层:6 句话验证
  - "TSLA 下个月期权链"
  - "AAPL 2025-01-17 的 call 期权 strike 多少"(双步:先 chain 再 quote)
  - "700.HK 的窝轮"
  - "腾讯牛熊证"(LLM 应识别"牛熊证" = warrant-list 700.HK)
  - "AAPL250117C190000 IV 多少"
  - "港股窝轮发行商"

## 已知 trade-off

- 期权合约符的两步发现(chain → quote)对 LLM 是个挑战,SKILL.md 必须给清晰示例。
- 期权 / 窝轮的中文术语映射多(认购证 = call、认沽证 = put、牛证 = bull、熊证 = bear、call 价 ≠ Strike),全靠 LLM 自有知识,不在 cli.py 做映射。
- 美股期权代码格式 vs 港股期权代码格式不同;cli.py 不校验合约符格式(交给 longbridge),只在 SKILL.md 里描述用法。
