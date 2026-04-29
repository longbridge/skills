# 获取数据的规则

数据获取优先级：**CLI（首选）→ MCP（次选）→ Web Search（兜底）**

- CLI 文档: https://open.longbridge.com/zh-CN/docs/cli/
- MCP Endpoint: `https://openapi.longbridge.com/mcp`
- MCP 文档: https://open.longbridge.com/docs

## 通用说明

**证券代码格式**: `{symbol}.{market}`
- 美股: `NVDA.US` / 港股: `0700.HK` / A股: `600519.SH` / 新加坡: `D05.SG`

**Rate Limit**: Quote API 每秒不超过10次，并发不超过5

---

## 目录
1. [维度1: 财务与业绩](#维度1-财务与业绩)
2. [维度2: 资金与交易](#维度2-资金与交易)
3. [维度3: 内部人与机构](#维度3-内部人与机构)
4. [维度4: 政策与监管](#维度4-政策与监管)
5. [维度5: 公司事件](#维度5-公司事件)
6. [维度6: 市场情绪](#维度6-市场情绪)
7. [维度7: 技术面](#维度7-技术面)
8. [用户数据（自选股+持仓）](#用户数据)

---

## 维度1: 财务与业绩

### CLI（首选）

```bash
# 财务报表（利润表/资产负债表/现金流）
longbridge financial-report {symbol}.{market} --kind IS          # IS=利润表, BS=资产负债表, CF=现金流
longbridge financial-report {symbol}.{market} --kind IS --report qf  # af=年报, saf=半年报, qf=季报
longbridge financial-report {symbol}.{market} --format json

# 经营数据摘要（营收/净利/EPS同比）
longbridge operating {symbol}.{market}
longbridge operating {symbol}.{market} --report af,qf --format json

# 一致预期（分析师共识：营收/EBIT/EPS多季度对比，含beat/miss标记）
longbridge consensus {symbol}.{market}
longbridge consensus {symbol}.{market} --format json

# EPS一致预期快照（均值/中位数/最高最低/上下调修正数量）
longbridge forecast-eps {symbol}.{market}
longbridge forecast-eps {symbol}.{market} --format json

# 财务日历（财报发布日期/业绩指引）
longbridge finance-calendar financial --symbol {symbol}.{market}
longbridge finance-calendar report --symbol {symbol}.{market}
longbridge finance-calendar macrodata --star 3       # 重要宏观数据发布
```

**关键输出字段**:
- `financial-report`: EPS, ROE, Revenue, Net Income, Gross Margin, Net Margin
- `operating`: 营业收入 + yoy, 净利润 + yoy, 每股收益 + yoy
- `consensus`: metric → estimate（含 beat/miss 标记）
- `forecast-eps`: mean, median, highest, lowest, up/down（修正趋势）

### MCP（CLI 不覆盖时）

- `get_financial_statements` — 更细粒度字段（`fields[].yoy` 同比）
- `get_stock_consensus` — 带参数控制年份/季度/报告类型
- `Security Filings` — 财报公告原文/链接

### Web Search（兜底）

- 财报日期确认（MCP仅覆盖已发布文件，未来财报日需搜索）
- 管理层 Guidance 修订原文（结构化数据不含 guidance 文本）

---

## 维度2: 资金与交易

### CLI（首选）

```bash
# 实时行情（价格/成交量/涨跌幅，含美股盘前盘后）
longbridge quote {symbol}.{market}
longbridge quote TSLA.US NVDA.US 700.HK          # 支持同时查多标的
longbridge quote {symbol}.{market} --format json

# 分时行情（逐分钟价格+成交量）
longbridge intraday {symbol}.{market}
longbridge intraday {symbol}.{market} --session all   # 含盘前盘后
longbridge intraday {symbol}.{market} --date 20260401

# 资金流向（大单/中单/小单流入流出）
longbridge capital {symbol}.{market}             # 资金分布快照
longbridge capital {symbol}.{market} --flow      # 逐分钟资金流时序

# 市场异动（急涨急跌/大单买卖异动）
longbridge anomaly --market US
longbridge anomaly --market HK --symbol {symbol}.{market}
longbridge anomaly --market CN --count 20

# 成交分布统计（按价位的买卖方成交量）
longbridge trade-stats {symbol}.{market}

# 港股经纪商持仓（仅HK）
longbridge broker-holding {symbol}.HK
longbridge broker-holding {symbol}.HK --period rct_5   # 近5日
longbridge broker-holding detail {symbol}.HK
```

**关键输出字段**:
- `quote`: last_done, prev_close, volume, turnover, pre/post_market_quote（美股）
- `capital dist`: capital_in/out（large/medium/small 各档）
- `anomaly`: alert（大笔买入/卖出/急速拉升）, emotion（Bull/Bear）

### MCP（CLI 不覆盖时）

- `Security Candlesticks` — K线复权/历史
- `Option Chain + Option Quote` — 美股期权链详细数据 [US]
- `Warrant Quote + Warrant Filter` — 港股窝轮/牛熊证 [HK]

### Web Search（兜底）

- A股: 龙虎榜、北向/南向资金个股明细、融资融券余额 [CN]
- 港股: 沽空详细数据 [HK]

---

## 维度3: 内部人与机构

### CLI（首选）

```bash
# 内部人交易（SEC Form 4，仅美股）
longbridge insider-trades {symbol}.US
longbridge insider-trades {symbol}.US --count 40 --format json

# 主要股东持仓（增持/减持/全部）
longbridge shareholder {symbol}.{market}
longbridge shareholder {symbol}.{market} --range inc    # 仅增持
longbridge shareholder {symbol}.{market} --range dec --sort chg

# 基金/ETF持仓（持有该股票的基金，按权重排列）
longbridge fund-holder {symbol}.{market}
longbridge fund-holder {symbol}.{market} --count 50

# 机构投资者13F持仓（仅美股）
longbridge investors                                     # Top 50 活跃基金经理
longbridge investors {cik}                               # 特定基金持仓明细
longbridge investors changes {cik}                       # 季度变化（NEW/ADDED/REDUCED/EXITED）
longbridge investors changes {cik} --from 2024-12-31

# 美股做空数据（空头比例/days-to-cover）
longbridge short-positions {symbol}.US
longbridge short-positions {symbol}.US --count 50 --format json
```

**关键输出字段**:
- `insider-trades`: filer, title, type（BUY/SELL/EXERCISE）, shares, price, value, owned_after
- `shareholder`: shareholder, % shares, chg shares, report_date
- `investors changes`: action, company, shares_change, value_change
- `short-positions`: rate%, short_shares, days_cover

**信号判断**:
- 多名内部人30天内集中买入 → 强正向信号
- CEO/CFO 大额卖出（排除期权行权后常规卖出）→ 负向信号
- 前5大股东任一显著减持 → 高优先级预警
- days_cover 持续攀升 → 做空压力增加 [US]

### MCP（CLI 不覆盖时）

- `get_latest_insider_trading_details` — 港股/A股内部人交易
- `get_company_top20_shareholders_by_institution_type` — 按机构类型（对冲基金/共同基金/养老基金）分组

### Web Search（兜底）

- A股大股东减持预披露公告（监管要求预先公告，MCP更新有延迟）
- 港股内部人交易（披露易格式特殊）
- 13F季度持仓深度分析（季度更新）

---

## 维度4: 政策与监管

### CLI（首选）

```bash
# 监管文件/公告（SEC 8-K/10-K，港交所公告等）
longbridge filing list {symbol}.{market}
longbridge filing list {symbol}.{market} --count 20
longbridge filing detail {symbol}.{market} {id}         # 查看全文

# 新闻资讯（从标题筛选政策/监管关键词）
longbridge news {symbol}.{market}
longbridge news {symbol}.{market} --count 20 --format json
longbridge news detail {article_id}                      # 查看新闻全文
```

**政策关键词过滤（筛选 filing/news 时使用）**:
- US: regulation, SEC, FDA approval, antitrust, tariff, sanction, export control, FTC, DOJ, CFIUS
- HK: 监管, 证监会, 港交所, 合规, 制裁, 关税, 反垄断, 国安法, 跨境数据
- CN: 监管, 政策, 发改委, 工信部, 证监会, 反垄断, 集采, 双减, 数据安全, 处罚, 约谈, 国产替代
- SG: MAS, regulation, compliance, sanction

### MCP（CLI 不覆盖时）

- `SocialMCPServiceGetTickerNewsArticles` — 按关键词精准搜索新闻

### Web Search（兜底）

- 政策深度解读与关联判断（尤其是 CN 市场重大政策）

---

## 维度5: 公司事件

### CLI（首选）

```bash
# 监管文件（并购/管理层变更/回购/增发等公告）
longbridge filing list {symbol}.{market}
longbridge filing detail {symbol}.{market} {id}

# 新闻（事件相关报道）
longbridge news {symbol}.{market} --count 20

# 财务日历（股息除权/IPO）
longbridge finance-calendar dividend --symbol {symbol}.{market}
longbridge finance-calendar ipo --market US
```

### Web Search（兜底）

- 传闻阶段的并购、尚未公告的管理层变更

---

## 维度6: 市场情绪

### CLI（首选）

```bash
# 市场情绪温度（0-100分，含估值/情绪分项）
longbridge market-temp US
longbridge market-temp HK
longbridge market-temp CN
longbridge market-temp US --history --start 2026-04-01 --end 2026-04-28 --format json

# 分析师评级（一致性评级/目标价/评级分布）
longbridge institution-rating {symbol}.{market}
longbridge institution-rating detail {symbol}.{market}  # 历史评级趋势+目标价
longbridge institution-rating {symbol}.{market} --format json

# 市场异动（异常大单/急速拉升，辅助情绪判断）
longbridge anomaly --market US --count 20
```

**关键输出字段**:
- `market-temp`: Temperature（0-100）, Description, Valuation, Sentiment
- `institution-rating`: recommend, target, change, strong_buy/buy/hold/sell/total

### MCP（CLI 不覆盖时）

- `Community Topics` — 社区讨论热度

### Web Search（兜底）

- 做空报告（Hindenburg、Citron 等，低频但高重要性）

---

## 维度7: 技术面

### CLI（首选）

```bash
# K线数据（支持1m/5m/15m/30m/1h/day/week/month/year）
longbridge kline {symbol}.{market} --period day --count 60
longbridge kline {symbol}.{market} --period 1h --count 48
longbridge kline {symbol}.{market} --adjust forward      # 前复权
longbridge kline history {symbol}.{market} --period day --start 2025-01-01 --end 2025-03-31

# 财务技术指标（PE/PB/换手率/市值/希腊值）
longbridge calc-index {symbol}.{market}
longbridge calc-index {symbol}.{market} --fields pe,pb,turnover_rate,total_market_value
longbridge calc-index {symbol}.{market} --fields volume_ratio,amplitude,five_day_change_rate

# 估值分析（含行业对比/历史百分位）
longbridge valuation {symbol}.{market}
longbridge valuation {symbol}.{market} --indicator pe --history --range 5
longbridge industry-valuation {symbol}.{market}
longbridge industry-valuation dist {symbol}.{market}    # 行业百分位排名
```

**calc-index 常用指标**:
`pe`, `pe_ttm`, `pb`, `ps`, `dps_rate`（股息率）, `turnover_rate`, `total_market_value`, `volume_ratio`（量比）, `amplitude`（振幅）, `five_day_change_rate`, `implied_volatility`（期权IV）

### MCP（CLI 不覆盖时）

- `GetInfraIndicator` — 技术指标信号（MACD金叉/RSI超买/布林带突破等 conditions 直接返回）
- `History Candlesticks` — 超长周期历史K线（52周高低点）

---

## 用户数据

### CLI（首选）

```bash
# 自选股管理
longbridge watchlist                                     # 列出所有自选股组
longbridge watchlist show {id}                           # 查看指定组
longbridge watchlist update {id} --add {symbol}.{market} # 添加
longbridge watchlist update {id} --remove {symbol}       # 删除
longbridge watchlist pin {symbol}.{market}               # 置顶

# 社区股票单
longbridge sharelist popular                             # 热门股票单
longbridge sharelist detail {id}
```

### MCP（CLI 不覆盖时）

- `Watchlist Groups API` — 获取自选股列表（含分组结构）
- `Stock Positions API` — 用户实际持仓（计算关联度权重）
- `Account Assets API` — 账户总资产（计算个股持仓占比）
