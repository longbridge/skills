# Output templates — 五类报告 · 标签翻译表 · 数据来源明细附录范式 · 免责声明

Loaded by `longbridge-hkipo-analysis` SKILL.md on demand. Use section order verbatim; the **「数据来源明细」附录是强制输出**，不论走哪条分支都必须在结尾出现。

> **Single-language output (mandatory)**: render the entire report — every heading, label, narrative paragraph, table cell, action frame, appendix row, and disclaimer — in **one** language matching the user's input (Simplified Chinese, Traditional Chinese, or English). Do NOT mix languages within a single response. The canonical layout below is written in Simplified Chinese; before emitting, translate every label, value, and disclaimer into the user's language using [§Label translation lookup](#label-translation-lookup) and [§Disclaimer variants](#disclaimer-variants).

---

## Label translation lookup

| 简体中文 (canonical) | 繁體中文 | English |
|---|---|---|
| 港股打新分析 | 港股打新分析 | HK IPO Subscription Analysis |
| 截至 | 截至 | As of |
| 当前价 | 當前價 | Current price |
| 币种 | 幣種 | Currency |
| 来源 | 來源 | Source |
| 评级 | 評級 | Rating |
| 推荐打新 | 推薦打新 | Recommended |
| 中性观望 | 中性觀望 | Neutral |
| 建议回避 | 建議迴避 | Avoid |
| 数据不足，无法评级 | 資料不足，無法評級 | Insufficient data — no rating |
| 综合评分 | 綜合評分 | Composite score |
| 核心理由 | 核心理由 | Core reasoning |
| 核心数据 | 核心數據 | Key data |
| 发行价 / 价格区间 | 發行價 / 價格區間 | Offer price / range |
| 认购期间 | 認購期間 | Subscription window |
| 上市日期 | 上市日期 | Listing date |
| 募资规模 | 募資規模 | Funds raised |
| 发行后市值 | 發行後市值 | Post-IPO market cap |
| 主承销商 | 主承銷商 | Lead underwriter |
| 行业 | 行業 | Industry |
| 四维评分 | 四維評分 | Four-dimension scoring |
| 定价合理性 | 定價合理性 | Valuation |
| 发行质量 | 發行質量 | Issue quality |
| 市场时机 | 市場時機 | Market timing |
| 基本面展望 | 基本面展望 | Fundamentals outlook |
| 强 / 中 / 弱 | 強 / 中 / 弱 | Strong / Medium / Weak |
| 招股书精华 | 招股書精華 | Prospectus highlights |
| 行业空间 | 行業空間 | Market space |
| 商业模式 | 商業模式 | Business model |
| 三年财务 | 三年財務 | 3-year financials |
| 营收 | 營收 | Revenue |
| 同比增速 | 同比增速 | YoY growth |
| 毛利率 | 毛利率 | Gross margin |
| 净利润 / 净亏损 | 淨利潤 / 淨虧損 | Net income / loss |
| 经营现金流 | 經營現金流 | Operating cash flow |
| 募资用途 | 募資用途 | Use of proceeds |
| 增长驱动 | 增長驅動 | Growth drivers |
| 盈利路径 | 盈利路徑 | Path to profitability |
| 管理层背景 | 管理層背景 | Management background |
| 主要风险 | 主要風險 | Main risks |
| 申购参考 | 申購參考 | Subscription reference |
| 稳健型 | 穩健型 | Conservative |
| 进取型 | 進取型 | Aggressive |
| 孖展提示 | 孖展提示 | Margin financing note |
| 打新日历 | 打新日曆 | IPO calendar |
| 公司名 | 公司名 | Company |
| 认购截止 | 認購截止 | Subscription close |
| 评级 | 評級 | Rating |
| 重点关注 | 重點關注 | Top picks |
| 市场整体打新环境 | 市場整體打新環境 | Overall IPO climate |
| 次新股追涨判断 | 次新股追漲判斷 | Recent-IPO chase assessment |
| 首日实际表现 | 首日實際表現 | First-day actual print |
| 暗盘溢价 | 暗盤溢價 | Grey-market premium |
| 偏离发行价 | 偏離發行價 | Deviation vs offer price |
| 参考目标价区间 | 參考目標價區間 | Reference price band |
| 数据来源明细 | 數據來源明細 | Data Source Appendix |
| 字段类别 | 欄位類別 | Field group |
| 抓取时间 | 抓取時間 | Fetch time |
| 数据期间 | 數據期間 | Period |
| 未披露 | 未披露 | Not disclosed |
| 待公告 | 待公告 | Awaiting disclosure |
| 不可得 | 不可得 | Unavailable |
| 估算 | 估算 | Estimated |
| 延伸查询 | 延伸查詢 | Further queries |

Source-identifier values — CLI 子命令名、MCP 工具名、URL、抓取时间戳 — 保持原样不翻译，只翻译"字段类别"列。

---

## 场景 A — 单只新股深度分析 (canonical, Simplified Chinese)

```
{公司名} ({代码}.HK) — 港股打新分析
截至：YYYY-MM-DD HH:MM   币种：HKD   来源：Longbridge Securities + WebSearch（详见附录）

【评级】{⭐ 推荐打新 | 🟡 中性观望 | ⚠️ 建议回避}    综合评分：{X.X} / 10

[核心理由]
{1–2 句话总结评级所依据的关键事实，必须挂钩具体数字。
 例："发行 PE 22 倍 vs 同业中位 28 倍，折价 21%；基石覆盖 38%（含 GIC + 高瓴）；
      公开发售超购倍数尚未公布，本轮评分基于已披露口径。"}

[核心数据]
┌──────────────────┬─────────────────┬──────────────────┐
│ 发行价格 / 区间    │ 认购期间          │ 上市日期           │
│ HKD {p_low}–{p_high}│ {YYYY-MM-DD}–{DD}│ {YYYY-MM-DD}     │
├──────────────────┼─────────────────┼──────────────────┤
│ 募资规模          │ 发行后市值        │ 主承销商           │
│ {amt} 亿港元      │ {amt} 亿港元      │ {投行 1 / 投行 2}  │
├──────────────────┼─────────────────┼──────────────────┤
│ 行业             │ 上市板块          │ 招股书披露易链接    │
│ {行业}           │ Main Board / GEM │ {URL}             │
└──────────────────┴─────────────────┴──────────────────┘

[四维评分明细]
定价合理性 ({a}/4.0)：{强 | 中 | 弱} — 发行 PE {x}× vs 同业中位 {y}×；
                                       发行 PS {x}× vs 同业 {y}×；
                                       定价处于价格区间 {上半段 | 中位 | 下半段}。
发行质量 ({b}/3.5)：{强 | 中 | 弱} — 基石比例 {x}%（含 {一线 / 腰部 / 关联方}）；
                                     国际配售超购 {y}× / 公开发售超购 {z}×（{已公布 | 等待公告}）；
                                     主承销商行业排名 {第 N 位}；锁定期 {N} 天。
市场时机 ({c}/2.0)：{强 | 中 | 弱} — 恒指近月 {±x}%；
                                     近 3 月港股新股破发率 {y}%；
                                     同行业板块近月 {±z}%。
基本面展望 ({d}/2.5)：{强 | 中 | 弱} — TAM {a} 亿港元、CAGR {b}%；
                                       营收 3 年 CAGR {c}%；毛利率 {d}%；
                                       募资用途中成长性投入占 {e}%（偿债占 {f}%）。

[招股书精华]

🌐 行业空间
   目标市场规模约 {amt}（{年份}），预计至 20XX 年达 {amt}，CAGR 约 {X}%。
   {一句行业地位描述，如"公司在 XX 细分占 X% 市占率，行业 TOP3"}。
   （来源：招股书 · 行业概况章节）

💼 这家公司靠什么赚钱（口语化 2–3 句）
   {示例："公司向连锁餐饮提供供应链管理 SaaS，按门店数年费收取费用，
     目前服务 XXX 家连锁，客户续费率 91%。"}

📊 近 3 年财务表
   ┌──────┬──────────┬────────┬───────┬──────────────┐
   │ 年份 │ 营收（亿） │ 同比 │ 毛利率 │ 净利润 / 净亏损│
   ├──────┼──────────┼────────┼───────┼──────────────┤
   │ 20{a}│ {x}      │ {y}%   │ {z}%  │ +{p} / -{p}  │
   │ 20{b}│ {x}      │ {y}%   │ {z}%  │ +{p} / -{p}  │
   │ 20{c}│ {x}      │ {y}%   │ {z}%  │ +{p} / -{p}  │
   └──────┴──────────┴────────┴───────┴──────────────┘
   关键趋势：{一句总结，如"营收高速增长但毛利率下行，亏损扩大，盈利路径需验证"}。
   （来源：招股书 · 财务摘要章节）

💸 募资用途
   ┌──────────────────┬───────┬──────────────────────┐
   │ 用途              │ 占比  │ 说明                 │
   ├──────────────────┼───────┼──────────────────────┤
   │ 研发投入          │ {x}% │ 开发 {产品/技术}      │
   │ 渠道 / 市场       │ {x}% │ 进入 {区域}           │
   │ 产能建设          │ {x}% │ 新建 {基地}           │
   │ 运营资金          │ {x}% │ 日常运营              │
   │ 偿还债务          │ {x}% │ {⚠️ > 30% 必须标红}   │
   └──────────────────┴───────┴──────────────────────┘
   （来源：招股书 · 募资用途章节）

🚀 增长驱动 TOP 3
   1. {驱动 1 — 一句话}
   2. {驱动 2}
   3. {驱动 3}
   （来源：招股书 · 未来发展策略章节）

💰 盈利路径（仅亏损公司输出，盈利公司隐藏此栏）
   {示例："公司当前尚未盈利，管理层在招股书中预期 20XX 年达经调整盈亏平衡，
     主要依赖规模效应 + 研发费用率下降"}
   ⚠️ {若招股书未给出明确时间线："盈利时间线不明确，属投资不确定性"}

👤 管理层背景
   - 创始人 / CEO：{姓名}，{背景：如"前 XX VP，行业经验 X 年，本次 IPO 前已完成 X 轮融资"}
   - 核心团队：{1–2 句}

[主要风险]
1. {风险 1 — 必须挂钩具体业务 / 财务事实，例："收入高度依赖 TOP3 客户，占比 58%，
                                          其中第一大客户为关联方，关联交易披露见招股书 P.XXX"}
2. {风险 2}
3. {风险 3}
{若评级 ≥ 中性 或 用户提到孖展，附加一条：
 "⚠️ 孖展（融资打新）会按杠杆放大破发损失：以 5 倍杠杆为例，若上市首日破发 10%，
   实际本金损失约 50%。"}

[申购参考]（仅供参考，不构成投资建议）
- 稳健型：{N} 手（自有资金）
- 进取型：≤ {M} 手，{若涉及孖展}：杠杆建议 ≤ 3 倍，且必须独立评估自身现金流
- {若评级 = ⚠️ 回避：不建议参与；若已认购可在港股规则允许的撤单期内考虑撤单}

[延伸查询]
- 看同业估值对比详情 → 调用 longbridge-peer-comparison
- 看公司完整招股书 → {港交所披露易 URL}
- 招股截止后重新评估（超购倍数公告后） → 重跑本 Skill

──────────────────────────────────────────────────────────────────
[数据来源明细]

| 字段类别                          | 来源                                                           | 抓取时间          | 数据期间             |
|----------------------------------|----------------------------------------------------------------|------------------|---------------------|
| 招股书摘要 / 发行价 / 时间线         | Longbridge `ipo detail {SYMBOL}`                              | YYYY-MM-DD HH:MM | 招股期               |
| 招股书章节原文                     | Longbridge `sec-filings {SYMBOL}` + HKEXnews `{URL}`            | YYYY-MM-DD HH:MM | 招股书发布日         |
| 同业估值 PE / PS / PB              | Longbridge `peer-comparison {SYMBOL}`                          | YYYY-MM-DD HH:MM | 前一交易日收盘       |
| 基石投资者名单                     | Longbridge `ipo detail {SYMBOL}` + `news {SYMBOL}`             | YYYY-MM-DD HH:MM | 招股期               |
| 主承销商行业排名                   | WebSearch — Dealogic HK IPO League Table 2024, {URL}            | YYYY-MM-DD HH:MM | 2024 年            |
| 国际配售 / 公开发售超购倍数         | Longbridge `ipo detail {SYMBOL}` {或 `[待公告]` 若尚未公布}     | YYYY-MM-DD HH:MM | 招股截止日          |
| 恒生指数近月行情                   | Longbridge `index-quote HSI.HK` + `kline HSI.HK`               | YYYY-MM-DD HH:MM | 近 60 个交易日      |
| 近 3 月港股新股首日表现 / 破发率    | Longbridge `ipo listed`                                        | YYYY-MM-DD HH:MM | 近 3 个月          |
| 同行业板块近月走势                 | Longbridge `sector-monitor` + `industry-overview {SECTOR}`      | YYYY-MM-DD HH:MM | 近 30 个交易日      |
| 公司基础信息 / 行业归属             | Longbridge `basicinfo {SYMBOL}` + `company-profile {SYMBOL}`    | YYYY-MM-DD HH:MM | 最新               |
| 招股相关舆情                       | Longbridge `news {SYMBOL}` + `topic {SYMBOL}`                  | YYYY-MM-DD HH:MM | 近 60 天           |
| 行业 TAM / CAGR（招股书外补强）    | WebSearch — {publisher}, {报告名}, {年份}, {URL}                | YYYY-MM-DD HH:MM | {报告年份}         |
| {…按需追加 WebSearch 行…}          | …                                                              | …                | …                   |

附录脚注约定：
- 每条 WebSearch 行必须包含 publisher + 报告 / 文章名 + 发布日期 + URL + 抓取时间。
- 招股书未披露的字段写 `[未披露]` 或 `[待公告]`；CLI / MCP / WebSearch 全都拿不到的写 `[不可得]`，并在主报告对应章节用定性描述代替。
- TAM 行若用「估算」（机构数据缺失时基于行业逻辑推算）必须显式写 `估算 — {基于哪些数据点}`，不得伪造机构来源。
- CLI / MCP 命令名 + URL + 时间戳保持原样不翻译，只翻译「字段类别」列。

──────────────────────────────────────────────────────────────────
{Disclaimer block — 见 §Disclaimer variants}
```

---

## 场景 B — 打新日历 (calendar mode)

```
📅 {港股打新日历 — 未来 4 周}
截至：YYYY-MM-DD HH:MM   来源：Longbridge Securities + WebSearch（详见附录）

┌──────────────────┬────────────┬────────────┬──────────┬─────────────┬──────────┐
│ 公司名 ({代码})   │ 认购截止    │ 上市日期    │ 募资规模 │ 行业         │ 评级     │
├──────────────────┼────────────┼────────────┼──────────┼─────────────┼──────────┤
│ {公司 A} (XXXX.HK)│ MM-DD      │ MM-DD      │ {amt}亿  │ {行业}       │ ⭐ 推荐  │
│ {公司 B} (XXXX.HK)│ MM-DD      │ MM-DD      │ {amt}亿  │ {行业}       │ 🟡 中性  │
│ {公司 C} (XXXX.HK)│ MM-DD      │ MM-DD      │ {amt}亿  │ {行业}       │ ⚠️ 回避  │
│ {公司 D} (XXXX.HK)│ MM-DD      │ MM-DD      │ {amt}亿  │ {行业}       │ ❌ 数据不足│
└──────────────────┴────────────┴────────────┴──────────┴─────────────┴──────────┘

【重点关注 — 1–2 只】
- {公司 A}：{一句理由，例如"发行 PE 折价 ≥ 20% + 基石 ≥ 30% + 行业 CAGR 25%"}
- {公司 B}：{若有第二只值得提示}

【市场整体打新环境】
- 近 3 月港股新股首日破发率：{X}%（{≤20% 健康 / 20-40% 一般 / >40% 差}）
- 恒指近月：{±x}%；同期港股 IPO 平均超购：{N}×
- 综合判断：{打新环境 好 / 一般 / 差}，{一句话建议如"建议优先选择基石机构强 + 定价折价的标的"}

──────────────────────────────────────────────────────────────────
[数据来源明细]

| 字段类别                  | 来源                                              | 抓取时间          | 数据期间      |
|---------------------------|---------------------------------------------------|------------------|--------------|
| 招股中新股列表             | Longbridge `ipo subscriptions`                    | YYYY-MM-DD HH:MM | 当前         |
| 待上市新股列表             | Longbridge `ipo wait-listing`                     | YYYY-MM-DD HH:MM | 当前         |
| 近期已上市破发率参考       | Longbridge `ipo listed`                           | YYYY-MM-DD HH:MM | 近 3 个月    |
| 恒指近月行情               | Longbridge `index-quote HSI.HK`                  | YYYY-MM-DD HH:MM | 近 60 交易日 |
| 单只评级背后数据           | 见各只单独运行本 Skill 时输出的附录                | —                | —            |
| {…按需追加…}              | …                                                | …                | …            |

──────────────────────────────────────────────────────────────────
{Disclaimer block — 见 §Disclaimer variants}
```

---

## 场景 C — 次新股追涨判断 (post-listing chase)

```
{公司名} ({代码}.HK) — 次新股追涨判断
截至：YYYY-MM-DD HH:MM   币种：HKD   当前价：{p}   发行价：{p0}
来源：Longbridge Securities + WebSearch（详见附录）

【当前位置】
- 距发行价偏离：{±XX.X}%
- 上市以来最高 / 最低：{p_h} / {p_l}
- 上市至今交易日数：{N}

【首日实际表现 + 暗盘】
- 暗盘溢价（{暗盘平台}）：{+X}%   暗盘日期：YYYY-MM-DD
- 首日开盘 / 收盘：{p_o} / {p_c}   首日振幅：{X}%
- 首日成交额 / 换手率：{amt} / {X}%

【简化四维评分】
定价合理性（当前价 vs 同业）：{强 | 中 | 弱} — 当前 PE {x}× vs 同业 {y}×
发行 / 上市质量：{强 | 中 | 弱} — 基石锁定期内 / 已解禁；首日溢价已包含 {X}% 情绪
市场时机：{强 | 中 | 弱} — 恒指近月 {±x}%；近 3 月破发率 {y}%
基本面展望：{强 | 中 | 弱} — TAM / CAGR / 营收增速等同场景 A 口径

【参考目标价区间】（仅基于同业估值倒推，区间非点位）
- 同业 PE 中位 {y}× × 公司 TTM EPS {e} ≈ 目标价 {p_target_pe}
- 同业 PS 中位 {y}× × 公司 TTM 营收 {r} / 总股本 {s} ≈ 目标价 {p_target_ps}
- **参考区间**：{p_low} – {p_high}（取上述两口径低 / 高端）

> 注意：以上区间为静态同业映射，未考虑公司具体溢价 / 折价因素，仅供作为思考锚，不构成目标价指令。

【主要风险】（次新股专项）
1. **流动性 / 解禁压力**：上市后 {N} 天，{若有锁定期信息}：基石 / 大股东锁定期至 YYYY-MM-DD
2. {公司特有业务风险，挂钩具体数字}
3. {追高情绪面风险，例如"首日溢价 {X}% 已透支 6–12 个月业绩兑现预期"}

【参考做法】（不构成买卖建议）
- 若当前价 < 参考区间下沿，且基本面未恶化：可作为观察候选，但分批介入控制单日仓位
- 若当前价 > 参考区间上沿：当前价已包含较多预期，等待回调或下次财报后重新评估
- 不建议短期追涨，尤其是单日涨幅 > 10% 的次新股

──────────────────────────────────────────────────────────────────
[数据来源明细]

| 字段类别                     | 来源                                              | 抓取时间          | 数据期间        |
|------------------------------|---------------------------------------------------|------------------|----------------|
| 招股书摘要 / 发行价          | Longbridge `ipo detail {SYMBOL}`                  | YYYY-MM-DD HH:MM | 招股期         |
| 上市后行情 / K 线            | Longbridge `quote {SYMBOL}` + `kline {SYMBOL}`     | YYYY-MM-DD HH:MM | 上市以来       |
| 首日开 / 收 / 振幅           | Longbridge `ipo listed` + `kline {SYMBOL}`        | YYYY-MM-DD HH:MM | 首日           |
| 暗盘溢价                    | WebSearch — 富途暗盘 / 辉立 / 耀才, {URL}, {日期}  | YYYY-MM-DD HH:MM | 上市前一日     |
| 同业估值                    | Longbridge `peer-comparison {SYMBOL}`             | YYYY-MM-DD HH:MM | 前一交易日     |
| 恒指 + 破发率参考            | Longbridge `index-quote HSI.HK` + `ipo listed`     | YYYY-MM-DD HH:MM | 近 60 / 90 天 |
| 锁定期 / 解禁                | Longbridge `sec-filings {SYMBOL}` + HKEXnews       | YYYY-MM-DD HH:MM | 招股书披露     |
| {…按需追加…}                 | …                                                 | …                | …              |

──────────────────────────────────────────────────────────────────
{Disclaimer block — 见 §Disclaimer variants}
```

---

## 异常 D — 数据不足，无法评级 (insufficient data)

```
{公司名} ({代码}.HK) — 港股打新分析
截至：YYYY-MM-DD HH:MM

❌ 数据不足，无法评级

【已尝试但缺失的关键字段】
- 发行价 / 价格区间：{已披露 | 未披露 | 待公告}
- 基石投资者比例：{已披露 | 未披露 | 待公告}
- 国际配售 / 公开发售超购倍数：{已披露 | 待公告（招股截止日下午）}
- {其他缺失关键字段}

【建议】
- 若招股期未结束：建议在招股截止日（{YYYY-MM-DD}）下午重新调用本 Skill，
  超购倍数公告后可补齐发行质量维度。
- 若招股书尚未在 HKEXnews 完整发布：等待招股书正式版后再分析。
- 也可单独查看：
   - 同业估值：调用 longbridge-peer-comparison
   - 公司基础信息：调用 longbridge-basicinfo
   - IPO 时间线：调用 longbridge-ipo `detail {SYMBOL}`

──────────────────────────────────────────────────────────────────
[数据来源明细]

| 字段类别                  | 来源                                              | 抓取时间          | 数据期间    |
|---------------------------|---------------------------------------------------|------------------|------------|
| {已成功获取的字段}         | {对应 CLI / MCP / WebSearch}                      | YYYY-MM-DD HH:MM | …          |
| {缺失字段 N}              | `[未披露]` 或 `[待公告]` 或 `[不可得]`             | YYYY-MM-DD HH:MM | —          |
| …                         | …                                                | …                | …          |

──────────────────────────────────────────────────────────────────
{Disclaimer block — 见 §Disclaimer variants}
```

---

## 异常 E — 拒绝接管 (out of scope)

```
{公司名 / 用户输入} — 港股打新分析

❌ 本 Skill 不接管此查询

【原因】
{从以下任选一条，简洁说明：}
- A — 非港股标的（{.US / .SH / .SZ / .SG}）
- B — 已上市 > 30 天，超出本 Skill 覆盖窗口
- C — 介绍上市（无募资），本 Skill 仅评估有募资的常规 IPO
- D — SPAC / De-SPAC，本 Skill 不覆盖
- E — 债券 / 优先股 / 仅 REIT 单独上市

【建议改用】
{按原因匹配 1–2 个 Skill：}
- 非港股 IPO → `longbridge-ipo`（覆盖 US / HK lifecycle）+ 二级市场分析 Skill
- 已上市 > 30 天 → `longbridge-stock-research` 或 `longbridge-fundamental`
- REIT → `longbridge-dcf` 或 `longbridge-stock-research`
- SPAC → `longbridge-stock-research`（按已上市处理）

──────────────────────────────────────────────────────────────────
[数据来源明细]

| 字段类别                  | 来源                                              | 抓取时间          | 数据期间   |
|---------------------------|---------------------------------------------------|------------------|-----------|
| 标的归属 / 上市状态        | Longbridge `basicinfo {SYMBOL}` + `quote {SYMBOL}` | YYYY-MM-DD HH:MM | 最新       |
| 上市日期                  | Longbridge `ipo detail {SYMBOL}` 或 `basicinfo`    | YYYY-MM-DD HH:MM | 最新       |

──────────────────────────────────────────────────────────────────
{Disclaimer block — 见 §Disclaimer variants}
```

---

## Disclaimer variants

Print exactly **one** variant matching the user's input language. Do not print multiple language versions in the same output.

**Simplified Chinese (zh-Hans)**

```
⚠️ 免责声明：本报告由 AI 基于港股打新四维评估框架与公开数据自动生成，仅供参考，
   不构成投资建议、要约或要约邀请，亦不代表 Longbridge Securities 任何官方判断。
   港股新股申购存在风险，包括但不限于上市首日破发、市场流动性不足、超购回拨等；
   孖展（融资）申购存在杠杆风险，亏损可能超过本金；招股书数据以港交所披露易官方
   文件为准，不同来源口径若有差异以披露易为准。投资有风险，入市需谨慎，历史表现
   不代表未来收益。请结合自身风险承受能力与资金使用周期独立做出投资决策。
```

**Traditional Chinese (zh-Hant)**

```
⚠️ 免責聲明：本報告由 AI 基於港股打新四維評估框架與公開資料自動生成，僅供參考，
   不構成投資建議、要約或要約邀請，亦不代表 Longbridge Securities 任何官方判斷。
   港股新股申購存在風險，包括但不限於上市首日破發、市場流動性不足、超購回撥等；
   孖展（融資）申購存在槓桿風險，虧損可能超過本金；招股書資料以港交所披露易官方
   文件為準，不同來源口徑若有差異以披露易為準。投資有風險，入市需謹慎，歷史表現
   不代表未來收益。請結合自身風險承受能力與資金使用週期獨立做出投資決策。
```

**English (en)**

```
⚠️ Disclaimer: This report is generated by AI using a four-dimension HK IPO subscription
   framework on public data. It is for reference only, does not constitute investment
   advice, an offer, or a solicitation, and does not reflect any official view of
   Longbridge Securities. HK IPO subscriptions carry risks, including first-day
   under-performance, market illiquidity, and claw-back from oversubscription; margin
   financing (孖展) introduces leverage risk and losses can exceed principal. Prospectus
   data is sourced from HKEXnews — where multiple sources diverge, the HKEXnews filing
   is authoritative. Past performance does not guarantee future results. Make your
   investment decisions independently based on your own risk tolerance and capital
   horizon.
```

---

## Anti-cheat reminders (output-side)

- 「数据来源明细」附录必须在每一类输出中出现，包括拒绝接管与数据不足分支。
- 任何 WebSearch 行缺 URL 或缺出处 → 该行降级为 `[不可得]`。
- 不在同一份报告中混用语言；所有标签、章节名、表格列、免责声明须一并翻译为用户输入语言。
- 评级标签必须是预设的 5 类之一（⭐ 推荐 / 🟡 中性 / ⚠️ 回避 / ❌ 数据不足 / ❌ 拒绝接管），不允许自创"略偏推荐"这种中间表述。
- 任何具体目标价（场景 C）必须以**区间**形式出现，且明确写明区间口径是同业映射、不是目标点位指令。
- 涉及孖展、融资、杠杆的输出必须包含杠杆放大损失的提示。
