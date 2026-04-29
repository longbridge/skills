---
name: longbridge-quote
description: |
  Real-time quotes, static reference, and valuation indices for stocks listed in HK / US / A-share / Singapore via Longbridge Securities. Returns last price, change, volume, turnover, market cap, industry, PE/PB, turnover-rate, and other indicators. Triggers: "现在多少钱", "股价", "涨跌幅", "成交量", "市值", "市盈率", "PE", "PB", "换手率", "行业", "現在多少", "股價", "成交量", "市值", "市盈率", "stock price", "current price", "quote", "market cap", "PE ratio", "valuation", "NVDA price", "AAPL quote", "茅台市值", "腾讯股价", "700.HK", "600519.SH".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-quote

Real-time quote, static info, and valuation indices for Longbridge-supported securities (HK / US / A-share / Singapore).

> **Response language**: respond in the user's input language — Simplified Chinese (简体中文), Traditional Chinese (繁體中文), or English. Keep symbols (`NVDA.US`, `700.HK`) and numeric values verbatim.

## When to use

Trigger on prompts asking about:

- Current price / change / volume — *"NVDA 现在多少钱"*, *"現在股價"*, *"What's NVDA's price?"*
- Industry / market cap / floats / EPS / BPS — *"贵州茅台市值多少"*, *"茅台屬於什麼行業"*, *"AAPL EPS"*
- Valuation indices (PE, PB, turnover rate, 5/10-day change, etc.) — *"NVDA 的 PE"*, *"700 換手率"*, *"AAPL volume ratio"*
- Trading status of a single security — *"AAPL still trading?"*, *"美股开盘了吗"*

For 2–5 symbol comparison defer to `longbridge-peer-comparison`. For historical valuation percentile, defer to `longbridge-valuation`.

## Symbol format

`<CODE>.<MARKET>`. Normalise before calling:

| Pattern | Market | Example |
|---|---|---|
| Uppercase ticker (US) | `.US` | `NVDA.US`, `AAPL.US` |
| 4-digit numeric | `.HK` | `700.HK`, `9988.HK` |
| 6-digit, starts `60` | `.SH` | `600519.SH` |
| 6-digit, starts `00`/`30` | `.SZ` | `300750.SZ` |
| Singapore ticker | `.SG` | `D05.SG` |
| Chinese / English company name | use knowledge | 腾讯 → `700.HK`, 特斯拉 → `TSLA.US`, 贵州茅台 → `600519.SH` |

If the market is ambiguous, **ask the user** rather than guessing.

## Workflow

1. Extract symbol(s) from the prompt; normalise each to `<CODE>.<MARKET>`.
2. Decide which info is required:
   - **Quote only** (price / change / volume) → default `cli.py -s ...`
   - **Static** (industry, market cap, EPS, BPS, dividend yield) → add `--include-static`
   - **Indices** (PE, PB, turnover rate, etc.) → add `--index pe,pb,turnover_rate,...`
   - **Combined** ("full snapshot") → both flags
3. Run via local CLI (preferred) or MCP fallback (see below).
4. Translate JSON to natural language; cite the source as **Longbridge Securities** / **数据来源:长桥证券** / **數據來源:長橋證券**.

## CLI

```bash
python3 scripts/cli.py -s NVDA.US -s 700.HK
python3 scripts/cli.py -s 600519.SH --include-static
python3 scripts/cli.py -s NVDA.US --index pe,pb,turnover_rate
python3 scripts/cli.py -s NVDA.US --include-static --index pe,pb,total_market_value
```

Common flags (all read-tier skills): `--longbridge-bin`, `--format json`, `--timeout 30`.

Full `--index` field list: see [references/calc-index-fields.md](references/calc-index-fields.md).

## Output

Success envelope:

```json
{
  "success": true,
  "source": "longbridge",
  "skill": "longbridge-quote",
  "skill_version": "1.0.0",
  "count": 2,
  "symbols": ["NVDA.US", "700.HK"],
  "datas": [{"symbol": "NVDA.US", ...}, {"symbol": "700.HK", ...}]
}
```

With `--include-static` / `--index`, each `datas[i]` becomes `{symbol, quote, static?, calc_index?}`. Missing per-symbol fields → `null` (not an error).

Error envelope: `{success: false, error_kind, error, details}`. See error table below.

## Error handling

| `error_kind` | What happened | Reply phrase (zh-Hans / zh-Hant / en) |
|---|---|---|
| `binary_not_found` | `longbridge` CLI not installed | "长桥 CLI 未安装,请先安装 longbridge-terminal" / "長橋 CLI 未安裝,請先安裝 longbridge-terminal" / "Longbridge CLI not installed: https://github.com/longportapp/longbridge-terminal" |
| `auth_expired` | OAuth token expired | "长桥登录态过期,请跑 `longbridge login`" / "登入過期,請執行 `longbridge login`" / "Login expired — run `longbridge login`." |
| `subprocess_failed` | Other CLI failure | "查询失败:<details.stderr>" / "查詢失敗:..." / "Query failed: <details.stderr>." |
| `no_input` | Required arg missing | "请告诉我要查的股票" / "請告訴我要查的股票" / "Tell me which symbol to query." |
| `invalid_input_format` | Symbol format wrong | "代码格式应为 `<CODE>.<MARKET>`,如 `NVDA.US`、`700.HK`" / similar zh-Hant / "Symbol must be `<CODE>.<MARKET>`, e.g. `NVDA.US`, `700.HK`." |

## MCP fallback

If `cli.py` returns `binary_not_found` and the user has run `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`, fall back to:

| CLI behaviour | MCP tool |
|---|---|
| `quote` subprocess | `mcp__longbridge__quote` |
| `static` subprocess | `mcp__longbridge__static_info` |
| `calc-index` subprocess | `mcp__longbridge__calc_indexes` |

MCP is slower (HTTP + OAuth) but works without a local binary.

## Related skills

| User asks | Route to |
|---|---|
| Candlestick / intraday chart | `longbridge-kline` |
| Orderbook depth / brokers / ticks | `longbridge-depth` |
| Capital flow / large-order distribution | `longbridge-capital-flow` |
| 2–5 symbol comparison | `longbridge-peer-comparison` |
| Historical PE/PB percentile | `longbridge-valuation` |
| Earnings / fundamentals | `longbridge-fundamental` |
| Recent news / filings | `longbridge-news` |

## File layout

```
longbridge-quote/
├── SKILL.md
├── references/
│   └── calc-index-fields.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
