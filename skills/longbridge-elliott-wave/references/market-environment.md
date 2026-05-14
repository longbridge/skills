# Market Environment Data Guide

Per-market data sources and signal interpretation for Module C.

> **CLI discovery rule**: before using any `longbridge` subcommand for the first time in
> a session, run `longbridge <subcommand> --help` to confirm flags and symbol format.
> Index codes (SPX, HSI, STI …) are **not** valid Longbridge symbols — use tracking ETFs
> as proxies (see tables below). If a proxy returns an error, fall back to Web Search.

## HK (HKEX)

| Signal | CLI approach | Suggested proxy | Web Search Fallback |
|--------|-------------|-----------------|---------------------|
| HSI trend (60-day) | `longbridge kline` — 60 daily bars, JSON | 2800.HK (Tracker Fund) | "恒生指数 今日" |
| Southbound flow (港股通净买入) | `longbridge capital` for target symbol | — | "南向资金 今日净买入" |
| Short-sell ratio | Not in CLI | — | "[stock name] HK short selling ratio site:hkex.com.hk" |
| H/A premium | `longbridge calc-index` for target symbol (check `--help` for fields) | — | "[company] AH溢价" |
| HK Dollar peg / HIBOR | Not in CLI | — | "HIBOR overnight rate" |
| CSRC / SFC regulatory news | `longbridge news` for target symbol | — | "[company] SFC regulatory" |

**Signal interpretation:**
- HSI above 20-day MA + southbound net inflow → supports bullish wave count
- Short-sell ratio > 20% → caution for longs; consistent with top-zone or Wave 5 late stage
- Wide H/A premium (H trading at discount to A) → H-share relatively cheap; supports reversal from bottom

## US (NYSE / NASDAQ)

| Signal | CLI approach | Suggested proxy | Web Search Fallback |
|--------|-------------|-----------------|---------------------|
| S&P 500 trend (60-day) | `longbridge kline` — 60 daily bars, JSON | SPY.US | "S&P 500 price today" |
| VIX level | Not in CLI | — | "VIX index current level" |
| CBOE put/call ratio | Not in CLI | — | "CBOE equity put call ratio" |
| Sector ETF (e.g. XLK, XLE) | `longbridge kline` — 30 daily bars, JSON | XLK.US, XLE.US etc. | Sector ETF price |
| Fed meeting calendar / rate expectations | Not in CLI | — | "FOMC next meeting date" |
| 10-year Treasury yield | Not in CLI | — | "US 10 year treasury yield" |

**Signal interpretation:**
- VIX > 25 → elevated fear; ABC corrections often complete near VIX spikes; supports bottom-zone count
- VIX < 15 → complacency; consistent with Wave 5 late stage / top-zone warning
- SPX in confirmed uptrend + sector ETF outperforming → confirms bullish impulse count
- Put/call > 1.0 → market fear; often contrarian buy signal at ABC completion

## A-share (SSE / SZSE)

| Signal | CLI approach | Suggested proxy | Web Search Fallback |
|--------|-------------|-----------------|---------------------|
| Shanghai Composite trend | `longbridge kline` — 60 daily bars, JSON | 000001.SH | "上证指数 今日" |
| Northbound flow (北向资金) | `longbridge capital` for target symbol | — | "北向资金 今日净买入 东方财富" |
| Margin balance (融资余额) | Not in CLI | — | "沪深两市融资余额 最新" |
| CSRC policy / meetings | `longbridge news` for target symbol | — | "证监会 最新政策" |
| Sector rotation | Not in CLI | — | "A股板块轮动 今日" |
| Short-sell ratio | Not widely available | — | "[stock name] 融券余额" |

**Signal interpretation:**
- Northbound net inflow > RMB 5bn on a single day → strong foreign buying; supports impulse count
- Northbound consecutive outflow (3+ days) → risk-off; supports corrective phase
- Margin balance rising rapidly → leverage building; often appears in Wave 3 or late Wave 5
- CSRC easing policy → positive catalyst; may trigger Wave 1 or Wave 3 start
- A-share circuit breaker (±10% daily limit): swings may be artificially suppressed — wave engine less reliable

**A-share specific warnings:**
- ST-prefixed stocks: refuse analysis
- Stocks with recent resumption from trading halt: refuse analysis (data gap distorts ZigZag)

## SGX (Singapore)

| Signal | CLI approach | Web Search Fallback |
|--------|-------------|---------------------|
| STI trend | `longbridge kline` — try a tracking ETF; CLI coverage for SGX may be limited | "Straits Times Index today" |
| SGX stock news | `longbridge news` for target symbol | "[company] SGX news" |
| SGD/USD rate | Not in CLI | "SGD USD exchange rate" |

**Note:** SGX CLI coverage may be limited. If `longbridge kline` returns an error or
insufficient data for an SGX symbol, fall back to Web Search and note "CLI data limited
for SGX" in the output.

## Web Search Quality Guidelines

When using Web Search for market environment data:
1. Prefer official sources: exchange websites, central bank, regulatory bodies
2. Secondary: Reuters, Bloomberg summaries, 财新, 东方财富
3. Always note the source in the output: "来源 / Source: [name]"
4. If Web Search also fails → mark the item as "数据不可用 / Data unavailable" — do not fabricate
5. Do not present Web Search results as the skill's own analysis — describe them as external data
