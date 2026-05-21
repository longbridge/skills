---
name: longbridge-strategy-optimizer
description: |
  Quantitative strategy generation and optimisation framework via Longbridge — create, modify, and backtest quant strategies: parameter grid search, walk-forward validation, overfitting detection (in-sample vs. out-of-sample), strategy combination (multi-strategy correlation diversification), Sharpe / Calmar ratio optimisation. Generates Python code frameworks for local execution. Triggers: "策略优化", "策略生成", "参数优化", "网格搜索", "回测优化", "过拟合", "walk-forward", "策略回测优化", "策略組合", "策略優化", "策略生成", "參數優化", "網格搜索", "回測優化", "strategy optimization", "strategy generation", "parameter optimization", "grid search", "overfitting", "walk-forward validation", "strategy backtest", "Sharpe ratio", "Calmar ratio".
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

# longbridge-strategy-optimizer

Quantitative strategy generation and optimisation framework — grid search, walk-forward validation, and overfitting detection.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking for:

- Building or optimising a quant strategy — *"帮我优化这个均线策略"*, *"strategy optimization"*, *"参数网格搜索"*
- Walk-forward or overfitting checks — *"走前验证"*, *"过拟合检测"*, *"walk-forward validation"*
- Strategy combination — *"多策略组合"*, *"strategy combination"*, *"correlation diversification"*
- Sharpe / Calmar ratio targets — *"最大化夏普比率"*, *"Calmar ratio optimisation"*

> **Note**: computation-intensive calculations should be executed locally. This skill generates the Python code framework; the user runs it on their own machine.

## Workflow

1. Clarify the strategy type (momentum / mean-reversion / breakout / factor) and target universe.
2. Fetch historical daily OHLCV data for the symbol(s).
3. Define the parameter search space.
4. Generate a Python framework that:
   - Implements the strategy logic
   - Runs `GridSearchCV`-style parameter sweep
   - Splits data into in-sample (IS) and out-of-sample (OOS) windows
   - Applies walk-forward validation (rolling IS/OOS windows)
   - Computes Sharpe, Calmar, max drawdown, and IS/OOS degradation ratio
   - Flags overfitting if OOS Sharpe < 0.5 × IS Sharpe
5. For multi-strategy combination: compute correlation matrix and suggest weights.
6. Present results as a parameter heatmap description and key metrics table.

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## CLI

```bash
# Daily OHLCV — backtest data (up to 500 trading days)
longbridge kline <SYMBOL> --period day --count 500 --format json
```

## Output structure

```
STRATEGY OPTIMISATION REPORT — <SYMBOL>  <Date>

STRATEGY: <Name / Type>
Universe:  <SYMBOL>
Period:    <start> – <end>  (xxx days)

PARAMETER SEARCH
Parameter       Range         Step    Best Value
fast_ma         5–50          5       xx
slow_ma         20–200        10      xxx
stop_loss       0.5%–5%       0.5%    x.x%

BEST RESULT (IN-SAMPLE)
Sharpe:  x.xx   Calmar:  x.xx   Max DD:  -xx.x%
CAGR:    xx.x%  Win Rate: xx.x%  Trades: xxx

OUT-OF-SAMPLE VALIDATION
Sharpe:  x.xx   Calmar:  x.xx   Max DD:  -xx.x%
IS/OOS Degradation: xx%  → [Acceptable | Possible Overfit | Overfit]

WALK-FORWARD SUMMARY
Window 1: IS Sharpe x.xx → OOS Sharpe x.xx
Window 2: IS Sharpe x.xx → OOS Sharpe x.xx
...

PYTHON CODE FRAMEWORK
<generated Python code>
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| Symbol not found | 未找到该代码，请确认市场和格式。 | 找不到該代碼，請確認市場和格式。 | Symbol not found — verify exchange and ticker. |
| Insufficient history | 历史数据不足，回测结果可靠性下降。 | 歷史數據不足，回測結果可靠性下降。 | Insufficient history — backtest reliability is reduced. |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-kline` — candlestick and OHLCV history
- `longbridge-execution-model` — realistic execution cost assumptions
- `longbridge-risk-return` — portfolio efficiency and risk-adjusted return
- `longbridge-capital-flow` — intraday volume and order flow signals

## File layout

```
skills/longbridge-strategy-optimizer/
└── SKILL.md
```
