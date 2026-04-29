# `--index` field reference

Pass any combination of these field names to `cli.py --index <a>,<b>,...`. Unknown names are silently ignored.

## Price / change

| Field | 简体中文 | 繁體中文 | English |
|---|---|---|---|
| `last_done` | 最新价 | 最新價 | Last price |
| `change_value` | 涨跌额 | 漲跌額 | Change value |
| `change_rate` | 涨跌幅 | 漲跌幅 | Change rate (%) |
| `volume` | 成交量 | 成交量 | Volume |
| `turnover` | 成交额 | 成交額 | Turnover |
| `ytd_change_rate` | 年初至今涨跌幅 | 年初至今漲跌幅 | YTD change rate |
| `five_minutes_change_rate` | 5 分钟涨跌幅 | 5 分鐘漲跌幅 | 5-min change |
| `five_day_change_rate` | 5 日涨跌幅 | 5 日漲跌幅 | 5-day change |
| `ten_day_change_rate` | 10 日涨跌幅 | 10 日漲跌幅 | 10-day change |
| `half_year_change_rate` | 半年涨跌幅 | 半年漲跌幅 | Half-year change |

## Liquidity / size

| Field | 简体中文 | 繁體中文 | English |
|---|---|---|---|
| `turnover_rate` | 换手率 | 換手率 | Turnover rate |
| `total_market_value` | 总市值 | 總市值 | Total market cap |
| `capital_flow` | 资金流向 | 資金流向 | Capital flow |
| `amplitude` | 振幅 | 振幅 | Amplitude |
| `volume_ratio` | 量比 | 量比 | Volume ratio |

## Valuation

| Field | 简体中文 | 繁體中文 | English |
|---|---|---|---|
| `pe` (alias `pe_ttm`) | 市盈率 PE (TTM) | 市盈率 PE (TTM) | PE (TTM) |
| `pb` | 市净率 PB | 市淨率 PB | PB |
| `eps` (alias `dividend_yield`) | EPS / 股息率 | EPS / 股息率 | EPS / dividend yield |

## Options & warrants Greeks

`implied_volatility`, `delta`, `gamma`, `theta`, `vega`, `rho`, `open_interest`, `expiry_date`, `strike_price`, `upper_strike_price`, `lower_strike_price`, `outstanding_qty`, `outstanding_ratio`, `premium`, `itm_otm`, `warrant_delta`, `call_price`, `to_call_price`, `effective_leverage`, `leverage_ratio`, `conversion_ratio`, `balance_point`.

For derivative-specific work, prefer `longbridge-derivatives`.
