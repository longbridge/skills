"""
APP.US Q2 FY2026 Earnings Preview
Run: python3 scripts/gen_app.py
Q1 2026 results released May 6, 2026 -- this report previews Q2 2026 (report date: Aug 5, 2026)
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.docx_builder import DocxBuilder
from scripts.chart_builder import ChartBuilder

OUTPUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "APP_Q2_FY2026_Earnings_Preview.docx"
)

b = DocxBuilder(
    symbol       = "APP.US",
    company      = "AppLovin Corp",
    report_date  = "2026年8月5日（盘后）",
    analysis_date= "2026年5月7日",
    price        = "$468.83",
    market_cap   = "~$1,577亿",
    valuation    = "P/E TTM 47.3x  |  EV/EBITDA ~30x",
    rating       = "强力买入（20位）| 买入（6位）| 持有（4位）  目标价 $638.50",
    output_path  = OUTPUT,
)
cb = ChartBuilder()

SECTIONS = [
    ("【一】", "上期业绩指引回顾（Q1 2026 实际）"),
    ("【二】", "管理层展望要点"),
    ("【三】", "上期电话会 | 分析师核心 Q&A"),
    ("【四】", "近期重要事件"),
    ("【五】", "历史指引兑现规律"),
    ("【六】", "市场一致预期 vs 管理层指引"),
    ("【七】", "本次财报核心关注点"),
    ("【八】", "风险提示"),
    ("附录",   "情景分析"),
]

b.cover()
b.toc(SECTIONS)

# ── 【一】上期业绩指引回顾 ─────────────────────────────────────────────────────
b.section("【一】上期业绩指引回顾（Q1 2026 实际）")
b.body("Q1 2026 结果于 2026年5月6日盘后发布，全面超预期。以下为管理层 Q4 2025 电话会（2026年2月11日）给出的 Q1 指引 vs. 实际对比。")

b.table(
    headers=["指标", "管理层指引（Q4 2025 电话会）", "Q1 2026 实际值", "与指引偏差", "评估"],
    rows=[
        ["营收",           "$1.745B–$1.775B（中值 $1.760B）", "$1.842B",   "+4.7%",   "超预期"],
        ["调整后 EBITDA",  "$1.465B–$1.495B（中值 $1.480B）", "$1.557B",   "+5.2%",   "超预期"],
        ["EBITDA 利润率",  "~84%",                             "85%",       "+100bps", "超预期"],
        ["净利润",         "未明确指引",                        "$1.206B",   "+109% YoY","超预期"],
        ["自由现金流",     "未明确指引",                        "$1.29B",    "FCF/净利≈107%", "超预期"],
        ["EPS（非GAAP）",  "未明确指引（隐含 ~$3.25）",        "$3.56",     "+9.5%",   "超预期"],
    ],
    col_widths=[1.4, 2.3, 1.2, 1.1, 0.9]
)

# Revenue trend chart (Q4 2024 - Q2 2026E)
rev_chart = cb.quarterly_bar(
    title="AppLovin Quarterly Revenue Trend (USD Billion)",
    quarters=["Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25", "Q1'26", "Q2'26E"],
    values=[1.00, 1.16, 1.26, 1.41, 1.66, 1.84, 1.93],
    estimate_idx=-1,
    ylabel="Revenue (USD Billion)",
)
b.image(rev_chart, width=6.0, caption="季度营收趋势（Q2 2026E 为管理层指引中值）")

b.subsection("关键财务亮点")
b.bullet("营收连续 6 季超出共识预期，平均超出幅度 +6%–+9%")
b.bullet("调整后 EBITDA 利润率达 85%，为公司历史最高，体现规模效应与低增量成本结构")
b.bullet("净利润 YoY +109%，增速远超营收增速，利润杠杆显著")
b.bullet("自由现金流 $1.29B，FCF 转化率约 107%（FCF/净利润），现金造血能力极强")
b.page_break()

# ── 【二】管理层展望要点 ──────────────────────────────────────────────────────
b.section("【二】管理层展望要点")
b.body("以下为管理层在 Q1 2026 电话会上发布的 Q2 2026 官方指引及战略要点。")
b.table(
    headers=["展望项目", "内容", "重要程度"],
    rows=[
        ["Q2 营收指引",         "$1.915B–$1.945B（中值 $1.93B，高于共识 +2.1%）",      "最高"],
        ["Q2 EBITDA 利润率",    "84%–85%，与 Q1 持平",                                  "最高"],
        ["Axon 全球自助上线",   "6月全球开放；AI 创意工具支持无人工自助投放全流程",     "最高 - 关键催化"],
        ["电商垂类加速",        "4月广告主消费创历史新高，超过历史最强 Q4 峰值",         "高"],
        ["回购计划",            "$23亿剩余授权，持续积极回购",                           "中"],
        ["Shelf 注册",          "5月6日提交混合货架注册（金额未披露），定性为战略弹性",  "中 - 需关注"],
    ],
    col_widths=[1.7, 3.3, 1.3]
)

# YoY growth trajectory
growth_chart = cb.growth_lines(
    title="Revenue & Adj. EBITDA Margin Trend",
    quarters=["Q1'25", "Q2'25", "Q3'25", "Q4'25", "Q1'26", "Q2'26E"],
    series=[
        {"label": "Revenue YoY Growth (%)", "color": "#1A56DB", "marker": "o",
         "values": [36, 25, 39, 44, 59, 53]},
        {"label": "Adj. EBITDA Margin (%)", "color": "#27AE60", "marker": "s",
         "values": [81, 75, 78, 81, 85, 84]},
    ],
    ylabel="% ",
)
b.image(growth_chart, width=6.0, caption="营收 YoY 增速 + 调整后 EBITDA 利润率趋势")
b.page_break()

# ── 【三】Q&A ──────────────────────────────────────────────────────────────────
b.section("【三】上期电话会 | 分析师核心 Q&A（Q1 2026 电话会 2026-05-06）")

b.qa(
    "Q1：Axon 自助投放6月全球上线，天花板如何估算？规模量化 KPI 是什么？",
    "CEO Foroughi：'14年来首次面向全球开放，广告主可自主注册并运营'。AI 创意工具支持全自动上户，早期内测合格线索转化率 57%，周消费增速约 50%。暂未给出年化体量预测。",
    "Q2 报告中：新增广告主数；自助投放营收占总广告收入比例；是否给出年化 TAM 扩展指引"
)
b.qa(
    "Q2：电商垂类与游戏广告是否存在内部蚕食？",
    "管理层明确：'目前完全没有看到蚕食'。电商和游戏广告主互不干扰，且数据量增加反而改善了两侧的定向精度。3月消费量比1月高约25%，4月创历史纪录。",
    "Q2 电商占总广告收入比例；游戏广告收入是否维持增速或加速"
)
b.qa(
    "Q3：85% EBITDA 利润率是否可持续？Axon 研发投入是否会压制利润率？",
    "Q2 指引 84%–85%，管理层未给出任何利润率下行预警。研发投入集中于 Axon 模型优化，低增量成本结构使利润率对营收增长高度敏感。",
    "Q2 实际 EBITDA 利润率 vs. 指引区间；R&D 占比变化"
)
b.qa(
    "Q4：Shelf 注册（5月6日）与 $23亿回购同时存在，资本配置逻辑是什么？",
    "电话会中未详细解释 Shelf 规模与用途。管理层将回购定性为主要资本回报方式，Shelf 定性为'战略灵活性储备'。",
    "Q2 报告前是否启动实际发行；Shelf 与回购的叙事一致性；是否有并购迹象"
)
b.page_break()

# ── 【四】近期重要事件 ────────────────────────────────────────────────────────
b.section("【四】近期重要事件")
b.table(
    headers=["日期", "来源", "事件", "关联性"],
    rows=[
        ["2026-05-06", "财报",    "Q1 营收 $1.842B 超预期 +4.2%；Q2 指引高于共识",
         "最大正面催化剂，盘后上涨 ~+10% 至 $514，后回落至 $467"],
        ["2026-05-06", "SEC",     "提交混合货架注册（规模未披露）",
         "短期稀释担忧；需关注后续是否实际启动发行"],
        ["2026-04",    "产品",    "Axon 自助投放内测启动；电商广告主周消费增速 50%",
         "核心增长驱动，验证 TAM 扩展逻辑"],
        ["2026-03",    "竞争",    "Google AI Max 广告系统升级；Meta Advantage+ 市场份额扩大",
         "竞争加剧风险，但 AppLovin 数据护城河短期难以复制"],
        ["持续",       "宏观",    "美联储降息预期推迟；关税不确定性影响广告主预算",
         "负面：广告主预算审慎；正面：CTV/程序化广告相对韧性"],
        ["持续",       "行业",    "移动游戏 DAU 全球平稳，强游戏（如 Supercell）持续表现",
         "支撑 AppLovin 核心游戏广告生态的稳定性"],
    ],
    col_widths=[0.9, 0.9, 2.5, 2.0]
)

# 60-day price action
price_data = json.load(open("/tmp/app_closes.json"))
dates  = [r["date"][5:] for r in price_data]
closes = [r["close"]    for r in price_data]
price_chart = cb.price_action(
    title="APP.US — 60-Day Price Action",
    dates=dates,
    prices=closes,
    current=closes[-1],
    current_label=f"${closes[-1]:.2f}",
    target=638.50,
    target_label="Consensus PT: $638.50",
    ylabel="Price (USD)",
)
b.image(price_chart, width=6.0, caption="APP.US 近60日股价走势（含共识目标价 $638.50）")
b.page_break()

# ── 【五】历史指引兑现规律 ────────────────────────────────────────────────────
b.section("【五】历史指引兑现规律")
b.body("AppLovin 管理层历次指引均属保守，实际结果连续超出。以下为近 5 季度营收指引 vs. 实际对比。")
b.table(
    headers=["季度", "指引中值", "实际营收", "超出幅度", "EBITDA 利润率实际"],
    rows=[
        ["Q1 2025", "~$1.07B", "$1.16B",  "+8.4%", "81%"],
        ["Q2 2025", "~$1.16B", "$1.26B",  "+8.6%", "75%"],
        ["Q3 2025", "~$1.30B", "$1.41B",  "+8.5%", "78%"],
        ["Q4 2025", "~$1.54B", "$1.66B",  "+7.8%", "81%"],
        ["Q1 2026", "~$1.75B", "$1.84B",  "+5.1%", "85%"],
        ["Q2 2026E","$1.93B（官方中值）", "—", "历史超出幅度预示可能实际达 $2.0B+", "84–85% 指引"],
    ],
    col_widths=[1.0, 1.3, 1.2, 1.2, 1.8]
)
b.bullet("营收指引兑现率：5/5 季度超出，平均超出幅度 +7.7%")
b.bullet("EBITDA 利润率：历次实际值均在指引区间内或高于上限")
b.bullet("EPS：6/6 季度超出非GAAP预期，平均 beat +8%")
b.bullet("本次指引可信度：极高——管理层一贯保守，$1.93B 中值大概率被超越，关注 $2.0B 门槛")

# EBITDA margin history bar chart
margin_chart = cb.quarterly_bar(
    title="Adj. EBITDA Margin by Quarter (%)",
    quarters=["Q1'25", "Q2'25", "Q3'25", "Q4'25", "Q1'26", "Q2'26E"],
    values=[81, 75, 78, 81, 85, 84],
    estimate_idx=-1,
    ylabel="Adj. EBITDA Margin (%)",
    color="#1A56DB",
    est_color="#F5A623",
)
b.image(margin_chart, width=5.5, caption="调整后 EBITDA 利润率历史趋势（Q2 2026E 为指引中值）")
b.page_break()

# ── 【六】市场一致预期 vs 管理层指引 ─────────────────────────────────────────
b.section("【六】市场一致预期 vs 管理层指引")
b.table(
    headers=["指标", "共识预期（发布前）", "管理层指引", "偏差分析"],
    rows=[
        ["营收",            "$1.89B",    "$1.915–1.945B（中值 $1.93B）",  "指引高于共识 +2.1%，超市场预期"],
        ["调整后 EBITDA",   "~$1.59B",   "$1.615–1.645B（中值 $1.63B）",  "指引高于共识 +1.6%"],
        ["EBITDA 利润率",   "~84%",      "84%–85%",                        "基本一致，偏保守"],
        ["EPS（非GAAP）",   "~$3.69",    "未明确（隐含约 $3.85–4.00）",   "实际可能再超共识 +5%+"],
        ["YoY 营收增速",    "+52%",      "+52%–+55%",                      "一致，增速仍处历史高位"],
        ["Axon KPI",        "无共识预期", "定性描述，无具体数字",           "最大预期差来源：披露质量"],
    ],
    col_widths=[1.5, 1.7, 2.1, 2.0]
)
b.body("预期差提示：Q2 财务数字预计小幅超出。真正的预期差在于 Axon 自助投放 6 月上线后的量化 KPI 披露——若管理层给出具体数据（新增广告主数、收入加速迹象），将是最大正向催化剂。")

# Peer comparison
peer_chart = cb.peer_multiples(
    title_left="P/E Ratio (TTM) Comparison",
    title_right="Revenue YoY Growth (%)",
    companies=["AppLovin", "Trade Desk", "IronSource (now Unity)", "Magnite", "Digital Turbine"],
    vals_left=[47.3, 65.2, None, 35.1, 18.4],
    vals_right=[59, 25, None, 18, 8],
    highlight="AppLovin",
    xlabel_left="P/E Ratio (TTM)",
    xlabel_right="Revenue YoY Growth (%)",
)
b.image(peer_chart, width=6.2, caption="同业估值 vs 增速对比（AppLovin 高估值对应高增速）")
b.page_break()

# ── 【七】核心关注点 ──────────────────────────────────────────────────────────
b.section("【七】本次财报核心关注点")
b.table(
    headers=["优先级", "关注点", "判断标准", "影响"],
    rows=[
        ["1 - 最高", "Axon 自助投放 Q2 KPI",
         "新增广告主数量；收入占比；若给出 >10% 软件营收来自自助 = 超强正面信号",
         "极高"],
        ["2 - 最高", "电商垂类增速持续性",
         "Q2 电商占广告收入 >20% 且环比加速 = 验证平台扩张；停滞 = 担忧 Q1 系一次性峰值",
         "极高"],
        ["3 - 高",   "EBITDA 利润率实际值",
         ">85% = 惊喜；84–85% = 符合预期；<82% = 估值重估风险",
         "高"],
        ["4 - 高",   "Shelf 注册后续",
         "是否实际启动发行；若未启动 + 回购继续 = 消除稀释担忧",
         "中-高"],
        ["5 - 中",   "Q3 2026 指引",
         "若中值 >$2.10B = 增速加速预期；若不及 $2.05B = 增速见顶担忧",
         "中"],
    ],
    col_widths=[1.0, 1.5, 3.2, 0.8]
)
b.page_break()

# ── 【八】风险提示 ────────────────────────────────────────────────────────────
b.section("【八】风险提示")
b.table(
    headers=["风险类型", "具体风险", "概率", "影响程度"],
    rows=[
        ["估值风险",   "P/E 47x、P/B 73x，增速或利润率任一放缓均触发大幅杀估值",    "中",    "极高"],
        ["竞争风险",   "Google AI Max + Meta Advantage+ 持续迭代，算法优势可能收窄", "中",    "高"],
        ["监管风险",   "FTC 对 AdTech 市场垄断调查；数据隐私新规影响定向精度",       "低-中", "高"],
        ["集中度风险", "核心客户为移动游戏广告主，游戏市场下行直接影响预算",         "低",    "高"],
        ["稀释风险",   "Shelf 注册规模未披露，若启动大规模发行叠加高估值放大冲击",   "低-中", "中-高"],
        ["做空风险",   "历史曾遭遇重大做空报告，若 Axon 数据受质疑可能引发剧烈波动", "低",    "极高"],
        ["宏观风险",   "关税/经济衰退导致广告主削减预算，尤其影响中小型游戏公司",    "中",    "中"],
    ],
    col_widths=[1.1, 3.0, 0.8, 0.9]
)

# ── 附录：情景分析 ────────────────────────────────────────────────────────────
b.section("附录 — 情景分析（Q2 2026 报告后）")
b.table(
    headers=["情景", "核心驱动", "关键数字", "股价预期反应"],
    rows=[
        ["牛市（30%）",
         "Axon KPI 超强 + 电商占比 >20% + 利润率 >85%",
         "营收 >$2.0B；EBITDA 利润率 86%+；Q3 指引 >$2.1B",
         "+20% ~ +30%（$560–610）"],
        ["基准（50%）",
         "财务超预期 +5%，Axon 渐进披露，利润率 84–85%",
         "营收 $1.95–2.0B；EBITDA 利润率 84%；Q3 指引 $2.05B",
         "+5% ~ +10%（$490–515）"],
        ["熊市（20%）",
         "Axon 自助上线不及预期 + 利润率 <83% + Shelf 实际发行",
         "营收 <$1.92B；EBITDA 利润率 82%；无 Axon 数据",
         "-10% ~ -20%（$375–420）"],
    ],
    col_widths=[1.1, 2.5, 2.2, 1.5]
)

scenario_chart = cb.scenario_hbar(
    title="Scenario Analysis: Implied Share Price Range (Q2 2026 Post-Earnings)",
    scenarios=["Bull Case (30%)", "Base Case (50%)", "Bear Case (20%)"],
    values=[585, 503, 398],
    current=468.83,
    current_label="$468.83",
    colors=["#27AE60", "#1A56DB", "#E74C3C"],
    xlabel="Implied Share Price (USD)",
)
b.image(scenario_chart, width=5.8, caption="Q2 2026 报告后情景分析：隐含股价区间")

# Analyst targets
analyst_chart = cb.analyst_pt_hbar(
    title="Analyst Price Targets vs Current Price",
    brokers=["Consensus (31 analysts)", "Highest (Bull)", "Goldman Sachs", "Morgan Stanley", "Lowest"],
    targets=[638.50, 860.00, 720.00, 650.00, 340.00],
    current=468.83,
    current_label="$468.83",
    colors=["#F5A623", "#27AE60", "#1A56DB", "#8E44AD", "#E74C3C"],
    xlabel="Target Price (USD)",
)
b.image(analyst_chart, width=5.8, caption="分析师目标价区间（共 31 位，共识 $638.50，+36%）")

b.disclaimer()
path = b.save()
print(f"已保存：{path}")
