# Field dictionary

When rendering financial figures from MCP responses, translate field names to the user's input language using this table.

## Income statement

| MCP field | 简体 | 繁體 | English |
|---|---|---|---|
| `revenue` / `total_revenue` | 营业收入 / 营收 | 營業收入 / 營收 | Revenue |
| `cost_of_revenue` | 营业成本 | 營業成本 | Cost of revenue |
| `gross_profit` | 毛利 | 毛利 | Gross profit |
| `operating_income` | 营业利润 | 營業利潤 | Operating income |
| `net_income` | 净利润 | 淨利潤 | Net income |
| `eps / eps_basic` | 每股收益 EPS | 每股盈利 EPS | EPS (basic) |
| `eps_diluted` | 摊薄每股收益 | 攤薄每股盈利 | EPS (diluted) |

## Balance sheet

| MCP field | 简体 | 繁體 | English |
|---|---|---|---|
| `total_assets` | 总资产 | 總資產 | Total assets |
| `total_liabilities` | 总负债 | 總負債 | Total liabilities |
| `total_equity` | 股东权益 | 股東權益 | Total equity |
| `bps / book_value` | 每股净资产 BPS | 每股淨資產 BPS | Book value per share |

## Cash flow

| MCP field | 简体 | 繁體 | English |
|---|---|---|---|
| `operating_cash_flow` | 经营性现金流 | 經營性現金流 | Operating cash flow |
| `investing_cash_flow` | 投资性现金流 | 投資性現金流 | Investing cash flow |
| `financing_cash_flow` | 筹资性现金流 | 籌資性現金流 | Financing cash flow |
| `free_cash_flow` | 自由现金流 | 自由現金流 | Free cash flow |

## Ratios

| MCP field | 简体 | 繁體 | English |
|---|---|---|---|
| `gross_margin` | 毛利率 | 毛利率 | Gross margin |
| `net_margin` | 净利率 | 淨利率 | Net margin |
| `operating_margin` | 营业利润率 | 營業利潤率 | Operating margin |
| `roe` | 净资产收益率 ROE | 淨資產收益率 ROE | Return on equity |
| `roa` | 总资产收益率 ROA | 總資產收益率 ROA | Return on assets |
| `roic` | 投入资本回报率 | 投入資本回報率 | Return on invested capital |
| `debt_to_equity` / `debt_ratio` | 资产负债率 | 資產負債率 | Debt-to-equity / debt ratio |
| `current_ratio` | 流动比率 | 流動比率 | Current ratio |
| `quick_ratio` | 速动比率 | 速動比率 | Quick ratio |

## Dividends & buybacks

| MCP field | 简体 | 繁體 | English |
|---|---|---|---|
| `dps / dividend_per_share` | 每股分红 DPS | 每股分紅 DPS | Dividend per share |
| `dividend_yield` | 股息率 | 股息率 | Dividend yield |
| `payout_ratio` | 派息率 | 派息率 | Payout ratio |
| `buyback_amount` | 回购金额 | 回購金額 | Buyback amount |

## Reporting metadata

| MCP field | 简体 | 繁體 | English |
|---|---|---|---|
| `fp_end` | 报告期末 | 報告期末 | Period end |
| `rpt_date` | 披露日期 | 披露日期 | Disclosure date |
| `currency` | 报告币种 | 報告幣種 | Reporting currency |
| `period` | 报告期 (年/季/半) | 報告期 (年/季/半) | Period (year / quarter / half) |
| `kind` | IS / BS / CF (利润表 / 资产负债表 / 现金流量表) | IS / BS / CF (利潤表 / 資產負債表 / 現金流量表) | Income statement / Balance sheet / Cash flow |

## Industry context

When the user is in a sector with non-standard accounting:

- **Banks / insurance**: high `debt_to_equity` is structural (deposits = liabilities). Read `roe` against industry, not absolute.
- **Tech / internet**: high `gross_margin` (60%+) is normal; `debt_to_equity` is typically 20–40%.
- **Cyclicals (steel, chemicals, energy)**: single-quarter `net_margin` swings widely; YoY only meaningful at cycle pivot.
- **Asset-heavy (airlines, manufacturing)**: negative `free_cash_flow` may signal capex investment, not weakness.

LLM should anchor explanations to **vs industry mean** or **vs own history**, not absolute thresholds.
