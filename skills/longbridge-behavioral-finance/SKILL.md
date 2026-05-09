---
name: longbridge-behavioral-finance
description: |
  Behavioral finance application framework — identify cognitive biases in markets (overreaction, underreaction, disposition effect, anchoring, herding), translate them into quantifiable trading signals (momentum / reversal), and assess whether current market sentiment shows systematic bias. Triggers: "行为金融", "认知偏差", "过度反应", "反应不足", "处置效应", "锚定效应", "羊群效应", "市场情绪偏差", "行為金融", "認知偏差", "過度反應", "反應不足", "處置效應", "錨定效應", "羊群效應", "behavioral finance", "cognitive bias", "overreaction", "underreaction", "disposition effect", "anchoring bias", "herding", "sentiment bias", "behavioral economics".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: read
---

# longbridge-behavioral-finance

Apply behavioral finance theory to identify exploitable market inefficiencies — map common cognitive biases to measurable price/volume patterns using Longbridge data.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"这只股票是不是过度反应了"*, *"did the market overreact to this news"*, *"這隻股票是否過度反應"*
- *"动量效应还是反转效应"*, *"momentum or reversal for this sector"*
- *"处置效应怎么影响散户行为"*, *"how does disposition effect affect retail traders"*
- *"现在市场有没有羊群效应"*, *"is there herding in the market right now"*
- *"锚定效应怎么影响股价"*, *"how does anchoring bias affect stock prices"*

For quantitative factor testing (IC/IR), use `longbridge-factor-research`. For market temperature index, use `longbridge-market-temp`.

## Bias catalogue and tradeable signals

### 1. Overreaction (过度反应)

**Theory**: Investors overweight recent bad/good news, pushing prices beyond fundamental value. De Bondt & Thaler (1985).

**Signal**: Long-term reversal. Stocks down 30–50% over 12M outperform over the next 12M; top performers underperform.

**Detect**:
```bash
longbridge kline <SYMBOL> --period day --count 252 --format json
```
Compare 12M return vs peer group. If a stock is in the bottom 10% of sector returns, screen for reversal setup.

### 2. Underreaction (反应不足)

**Theory**: Investors are slow to update beliefs; price drifts gradually toward fair value after earnings surprises.

**Signal**: Post-earnings announcement drift (PEAD). Buy after positive earnings surprise; price continues rising for 1–3 months.

**Detect**: Use `longbridge-earnings` to identify beats. Track price drift with `longbridge kline --period day --count 60`.

### 3. Disposition Effect (处置效应)

**Theory**: Investors sell winners too early and hold losers too long (Shefrin & Statman, 1985).

**Market impact**: Selling pressure on recent winners creates resistance near recent highs; support near cost basis concentrations.

**Detect**: High capital inflows after a price surge = retail profit-taking.
```bash
longbridge capital <SYMBOL> --format json
```

### 4. Anchoring Bias (锚定效应)

**Theory**: Investors anchor to arbitrary reference prices (52-week high, IPO price, round numbers).

**Signal**: 52-week high breakout tends to persist (stocks resist breaking prior highs but accelerate once broken).

**Detect**: Fetch 52-week high from `longbridge calc-index <SYMBOL> --format json` or static data.

### 5. Herding (羊群效应)

**Theory**: Investors follow the crowd, amplifying trends beyond fundamentals.

**Signal**: Abnormal volume + price acceleration without fundamental catalyst = herding. Also: analyst consensus clustering.

**Detect**:
```bash
longbridge market-temp --format json          # Market sentiment index 0-100
longbridge capital <SYMBOL> --format json     # Capital flow concentration
```

If market temperature > 80 and a single sector dominates capital inflow → herding warning.

### 6. Overconfidence (过度自信)

**Theory**: Investors overestimate precision of their forecasts, leading to under-diversification and excess trading.

**Market impact**: High turnover in bull markets; individual stocks show higher volatility than fundamentals justify.

**Detect**: Turnover rate spike from `longbridge quote <SYMBOL> --format json` (turnover_rate field).

## Workflow

1. Identify which bias the user is asking about (or scan all six).
2. Fetch relevant data (kline / market-temp / capital flow).
3. Map observed price/volume pattern to the bias.
4. Quantify signal strength: magnitude, duration, persistence.
5. Suggest a trading implication (entry / exit / avoid) with explicit caveats.

## CLI

```bash
longbridge kline --help
longbridge market-temp --help
longbridge capital --help

longbridge market-temp --format json
longbridge kline <SYMBOL> --period day --count 60 --format json
longbridge capital <SYMBOL> --format json
```

## Output

Present:
1. Identified bias and academic basis.
2. Observable evidence from Longbridge data (specific numbers).
3. Tradeable implication (signal direction, horizon, conviction).
4. Risks: when the bias does not persist (e.g. mean-reversion fails in trending markets).
5. Disclaimer: behavioral signals are probabilistic, not deterministic.

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 请安装 longbridge-terminal 或检查 MCP 配置。 | 請安裝 longbridge-terminal 或檢查 MCP 配置。 | Install longbridge-terminal or check MCP config. |
| stderr: `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |
| Insufficient price history | 历史数据不足，无法可靠识别偏差信号，请延长观察期。 | 歷史數據不足，請延長觀察期。 | Insufficient history to identify bias reliably; extend the lookback. |

## Related skills

- `longbridge-market-temp` — market sentiment temperature index
- `longbridge-capital-flow` — intraday capital flow and large/small order split
- `longbridge-factor-research` — quantitative factor IC/IR analysis
- `longbridge-anomaly` — unusual price/volume movements

## File layout

```
skills/longbridge-behavioral-finance/
└── SKILL.md
```
