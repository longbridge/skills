---
name: longbridge-derivatives
description: |
  Options (US / HK) and Hong Kong warrants (callable bull/bear, call warrants, put warrants) via Longbridge Securities — option quote, option chain by underlying / expiry, warrant quote / list / issuers. Returns IV, Greeks, strikes, expiries. Triggers: "期权", "option", "call", "put", "认购", "认沽", "行权价", "到期日", "IV", "希腊字母", "delta", "gamma", "窝轮", "牛熊证", "认购证", "认沽证", "認購", "認沽", "行權價", "到期日", "窩輪", "牛熊證", "option chain", "options expiry", "warrant", "CBBC", "callable bull bear contract".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-derivatives

Options (US / HK) and HK warrants. Underlying-stock quotes belong in `longbridge-quote`.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Subcommands

| Subcommand | Returns |
|---|---|
| `option-quote <contract> [<contract>...]` | Quote(s) for one or more option contracts (OCC symbols). Includes IV, delta, strike, expiry. |
| `option-chain <underlying>` | Available expiry dates for the underlying. |
| `option-chain <underlying> --date YYYY-MM-DD` | Strikes for a specific expiry — each row gives `call_symbol` and `put_symbol` OCC codes. |
| `warrant-quote <warrant> [<warrant>...]` | Quote(s) for HK warrants (leverage, IV, etc.). |
| `warrant-list <underlying>` | Warrants on a Hong Kong underlying (`underlying` must be `.HK`). |
| `warrant-issuers` | Directory of HK warrant issuers. |

## OCC option symbol

Format: `<TICKER><YYMMDD><C|P><STRIKE×1000, 8 digits>`. Example: `AAPL240119C190000` = AAPL, expires 2024-01-19, Call, strike $190.00.

## Two-step option discovery

| User input | Strategy |
|---|---|
| Full OCC symbol | `option-quote <symbol>` directly |
| Underlying + expiry + strike + call/put | `option-chain <ul> --date <d>` to find OCC code → `option-quote` |
| Underlying + window only | `option-chain <ul>` to list expiries; ask user to pick |

## Term mapping

| User says | Term |
|---|---|
| 认购证 / 牛证 / call | Call |
| 认沽证 / 熊证 / put | Put |
| 行权价 / strike | Strike |
| 到期日 / expiry | Expiry |
| 隐含波动率 / IV | Implied volatility |

## CLI

```bash
longbridge option-quote   AAPL250117C190000 AAPL250117P190000  --format json
longbridge option-chain   AAPL.US                              --format json
longbridge option-chain   AAPL.US --date 2025-01-17            --format json
longbridge warrant-quote  12345.HK                             --format json
longbridge warrant-list   700.HK                               --format json
longbridge warrant-issuers                                     --format json
```

## Output (per subcommand)

- `option-quote`: `count / contracts / datas` (each row: IV, delta, strike, expiry, …)
- `option-chain` (no date): `underlying / datas` — array of `{expiry_date}` objects
- `option-chain --date`: `underlying / date / datas` — rows of `{strike, call_symbol, put_symbol, standard}`
- `warrant-quote`: `count / warrants / datas`
- `warrant-list`: `underlying / datas` (array of `{symbol, name, type, expiry, last, leverage_ratio}`)
- `warrant-issuers`: `datas` (array of `{id, name_(cn), name_(en)}`)

## When to clarify

- Warrant query on a non-HK underlying → tell the user "warrants are HK-only" and route appropriately.
- Long strike list (>30) → present near-the-money strikes only.
- IV / Greeks during off-hours → may be a previous-session snapshot; mention this if the user asks for "real-time".

## MCP fallback

| CLI subcommand | MCP tool |
|---|---|
| `option-quote` | `mcp__longbridge__option_quote` |
| `option-chain` (no date) | `mcp__longbridge__option_chain_expiry_date_list` |
| `option-chain --date` | `mcp__longbridge__option_chain_info_by_date` |
| `warrant-quote` | `mcp__longbridge__warrant_quote` |
| `warrant-list` | `mcp__longbridge__warrant_list` |
| `warrant-issuers` | `mcp__longbridge__warrant_issuers` |

MCP-only extensions: `mcp__longbridge__option_volume`, `mcp__longbridge__option_volume_daily` (option volume analysis — not in CLI).

## Related skills

- Underlying quote / static → `longbridge-quote`
- Underlying candlesticks → `longbridge-kline`
- Underlying orderbook depth → `longbridge-depth`

## Error handling

If `longbridge` is missing, fall back to MCP. *"no quote access"* on `option-quote` indicates the account lacks the options market-data subscription — surface the message verbatim and tell the user to upgrade quote permissions on Longbridge.

## File layout

```
longbridge-derivatives/
└── SKILL.md          # prompt-only, no scripts/
```
