"""
CNL.US Q1 FY2026 Earnings Preview
Run: python3 scripts/gen_cnl.py
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.docx_builder import DocxBuilder
from scripts.chart_builder import ChartBuilder

OUTPUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "CNL_Q1_FY2026_Earnings_Preview.docx"
)

b = DocxBuilder(
    symbol       = "CNL.US",
    company      = "Collective Mining Ltd.",
    report_date  = "2026年5月21日（盘后）",
    analysis_date= "2026年5月7日",
    price        = "$18.05",
    market_cap   = "~$16.8亿",
    valuation    = "P/B 11.5x  |  P/E -32x（勘探阶段）",
    rating       = "强力买入（6位分析师）  |  目标价 $25.00",
    output_path  = OUTPUT,
)
cb = ChartBuilder()

SECTIONS = [
    ("【一】", "上期业绩指引回顾"),
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
b.section("【一】上期业绩指引回顾")
b.body("Collective Mining 为勘探阶段公司，无传统营收/利润指引。以运营里程碑 vs. 实际进展为核心评估基准。")

b.subsection("上期运营里程碑 vs. 实际进展")
b.table(
    headers=["里程碑 / 指标", "上期承诺 / 预期", "实际情况", "评估"],
    rows=[
        ["Apollo 系统北向扩张",  "向北延伸钻探",           "确认北向扩展 450m，新发现 Hanging Wall 矿脉带", "超预期"],
        ["Apollo 高品位截距",    "维持历史高品位水平",      "61.30m @ 1.78 g/t AuEq；130.40m @ 1.15 g/t AuEq", "超预期"],
        ["2026 钻探计划执行",    "Q1 推进 Hanging Wall",   "如期执行，Ramp Zone + 北部 Breccia 双线推进",     "按计划"],
        ["现金储备",             "$1.35亿（2025年12月）",  "Q1 报告待披露",                                   "待验证"],
        ["净亏损（EPS）",        "共识 -$0.12/股",         "Q1 报告待披露",                                   "待验证"],
    ],
    col_widths=[1.5, 1.6, 2.4, 0.8]
)

b.subsection("历史高品位钻探截距趋势")
# Chart: Apollo drill intercepts over time
drill_chart = cb.grouped_bar(
    title="Apollo System — Key Drill Intercepts (AuEq g/t)",
    categories=["Q2 2025", "Q3 2025 (HW)", "Q4 2025 (RZ)", "Q1 2026 (RZ)"],
    series=[
        {"label": "Grade (g/t AuEq)", "color": "#F5A623",
         "values": [1.12, 1.45, 1.15, 1.78]},
        {"label": "Width (m, /10)", "color": "#1A56DB",
         "values": [8.5, 7.8, 13.04, 6.13]},
    ],
    ylabel="Grade (g/t) / Width (m/10)",
)
b.image(drill_chart, width=5.8, caption="Apollo 系统历史钻探截距（品位 g/t AuEq + 厚度 m/10）")

b.subsection("最新共识财务预期（Q1 FY2026）")
b.table(
    headers=["指标", "共识预期", "说明"],
    rows=[
        ["营收",     "$0",          "勘探阶段，无产品销售收入"],
        ["EBIT",     "-$1,111万",   "勘探支出驱动"],
        ["净亏损",   "-$1,041万",   ""],
        ["EPS",      "-$0.12",      ""],
        ["调整后EPS","-$0.11",      ""],
    ],
    col_widths=[1.5, 1.5, 3.3]
)
b.page_break()

# ── 【二】管理层展望要点 ──────────────────────────────────────────────────────
b.section("【二】管理层展望要点")
b.table(
    headers=["展望项目", "内容", "重要程度"],
    rows=[
        ["2026 钻探目标",     "全年 100,000 米，Apollo 系统为核心（黄金+铜当量）",       "高"],
        ["资金状况",          "截至 2025年12月 现金 $1.35亿，宣称完全覆盖 2026 计划",   "高"],
        ["$5亿 Shelf 发行",   "2026年5月5日提交 S-3，为战略融资窗口（或运营缺口？）",   "高 - 关键风险"],
        ["GDXJ 纳入",         "加入 VanEck Junior Gold Miners ETF，提升机构可见度",     "中"],
        ["总部迁址",          "执行总部迁至迈阿密，国际化运营信号",                      "低"],
        ["股东大会",          "6月15日召开年度特别大会，含股权授权议案",                 "中"],
    ],
    col_widths=[1.5, 3.5, 1.3]
)

# Cash runway chart
cash_chart = cb.quarterly_bar(
    title="Cash Balance Trend (USD Million)",
    quarters=["Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026E"],
    values=[148, 142, 135, 120],
    estimate_idx=-1,
    ylabel="Cash (USD Million)",
    color="#1A56DB",
    est_color="#F5A623",
)
b.image(cash_chart, width=5.5, caption="现金余额趋势（Q1 2026E 为市场估算）")
b.page_break()

# ── 【三】Q&A ──────────────────────────────────────────────────────────────────
b.section("【三】上期电话会 | 分析师核心 Q&A")
b.body("CNL 不定期举行投资者电话会，以下为近期分析师重点关注话题及管理层公开回应。")

b.qa(
    "Q1：Apollo Ramp Zone 高品位截距能否支撑资源量升级（MRE Update）？",
    "截距 61.30m @ 1.78 g/t AuEq 持续扩张 Apollo 规模，管理层表示资源量有望实质性增加",
    "Q1 报告中是否宣布 MRE 更新时间表或初步数字"
)
b.qa(
    "Q2：$1.35亿现金已足够，为何同时注册 $5亿 Shelf？",
    "Shelf 为战略性融资窗口，不代表当前有融资需求，为并购或加速扩张预留灵活性",
    "电话会上追问 Shelf 使用意图；与现金充足表述的矛盾是否有清晰解释"
)
b.qa(
    "Q3：加入 GDXJ 后机构持仓变化如何？",
    "ETF 被动买入已部分体现，机构持股占比上升，流动性改善",
    "Q1 日均成交量是否从约 5 万股明显提升；机构持仓占比变化"
)
b.qa(
    "Q4：哥伦比亚运营风险（政策、许可）如何管控？",
    "管理层强调与当地社区关系稳固，许可证续期无重大障碍",
    "Q1 是否有任何许可或社区关系方面的新披露"
)
b.page_break()

# ── 【四】近期重要事件 ────────────────────────────────────────────────────────
b.section("【四】近期重要事件")
b.table(
    headers=["日期", "来源", "事件", "关联性"],
    rows=[
        ["2026-05-05", "SEC S-3",  "提交最高 $5亿混合货架发行",
         "最大短期风险：稀释担忧，股价当日 -3.8%（$17.67->$16.70）"],
        ["2026-04",    "公司公告", "加入 GDXJ ETF + 总部迁至迈阿密",
         "正面：指数被动买入 + 机构曝光度提升"],
        ["2026-04",    "钻探公告", "Apollo Ramp Zone：61.30m @ 1.78 g/t AuEq",
         "正面：持续验证高品位，资源量升级叙事强化"],
        ["2026-03",    "公司公告", "年度股东特别大会定于 6月15日",
         "含股权授权议案，与 Shelf 发行相关"],
        ["持续",       "宏观",     "黄金现货价格维持 $3,200+/oz",
         "正面：提升 Apollo 项目经济价值"],
        ["持续",       "行业",     "铜价高位震荡（Apollo 含铜当量）",
         "正面：多金属矿化提升项目综合价值"],
    ],
    col_widths=[0.9, 0.9, 2.2, 2.3]
)

# 60-day price action chart from kline data
price_data = json.load(open("/tmp/cnl_closes.json"))
dates  = [r["date"][5:] for r in price_data]   # MM-DD
closes = [r["close"]    for r in price_data]
price_chart = cb.price_action(
    title="CNL.US — 60-Day Price Action",
    dates=dates,
    prices=closes,
    current=closes[-1],
    current_label=f"${closes[-1]:.2f}",
    target=25.00,
    target_label="Consensus PT: $25.00",
    ylabel="Price (USD)",
)
b.image(price_chart, width=6.0, caption="CNL.US 近60日股价走势（含共识目标价）")
b.page_break()

# ── 【五】历史指引兑现规律 ────────────────────────────────────────────────────
b.section("【五】历史指引兑现规律")
b.body("勘探阶段公司，无传统收入/EPS 指引历史。以运营里程碑兑现率代替财务指引追踪。")
b.table(
    headers=["周期", "里程碑承诺", "实际兑现", "评级"],
    rows=[
        ["2026 Q1",  "Hanging Wall Vein Zone 钻探推进",    "高品位截距，Apollo 北向扩 450m",       "超预期"],
        ["2025 H2",  "Apollo 系统扩张 + Ramp Zone 新发现", "创纪录高品位截距，系统持续扩张",       "超预期"],
        ["2025 H1",  "100,000m 钻探计划部署",              "钻探机部署如期完成",                   "按计划"],
        ["现金管理", "充足现金覆盖 2026 计划",              "$1.35亿 + 同期注册 $5亿 Shelf",        "待观察"],
    ],
    col_widths=[0.9, 2.2, 2.5, 0.9]
)
b.bullet("钻探里程碑兑现率：3/3 周期按时或超预期，执行力评级：高")
b.bullet("资源量趋势：Apollo MRE 历次更新均向上修正，管理层估算偏保守")
b.bullet("本次指引可信度：运营执行高可信；$5亿 Shelf 与资金充足表述之间的矛盾需在电话会澄清")

# Analyst price target chart
analyst_chart = cb.analyst_pt_hbar(
    title="Analyst Price Targets vs Current Price",
    brokers=["Consensus (6 analysts)", "Canaccord Genuity", "Cormark Securities",
             "Haywood Securities", "PI Financial"],
    targets=[25.00, 28.00, 25.00, 24.00, 23.00],
    current=closes[-1],
    current_label=f"${closes[-1]:.2f}",
    colors=["#F5A623", "#8E44AD", "#27AE60", "#1A56DB", "#E74C3C"],
    xlabel="Target Price (USD)",
)
b.image(analyst_chart, width=5.8, caption="分析师目标价 vs 当前股价")
b.page_break()

# ── 【六】市场一致预期 vs 管理层指引 ─────────────────────────────────────────
b.section("【六】市场一致预期 vs 管理层指引")
b.table(
    headers=["指标", "市场预期", "管理层指引", "偏差分析"],
    rows=[
        ["营收",         "$0",          "无（勘探阶段）",        "一致，无预期差"],
        ["净亏损",       "~-$1,040万",  "未明确指引",            "参考现金消耗速率，变动有限"],
        ["EPS",          "-$0.12",      "未明确指引",            "小幅亏损，对股价影响微弱"],
        ["现金余额",     "~$1.2亿估算", "足够覆盖 2026 钻探",   "与 Shelf 意图存在叙事矛盾，电话会核心追问点"],
        ["Apollo MRE",   "更新期待中",  "未公告时间表",          "若随 Q1 报告披露初步数字，是最大正向催化剂"],
        ["2026 钻探进度","100,000m 全年","目标维持",             "季度进度披露是关注点"],
    ],
    col_widths=[1.3, 1.1, 1.5, 2.4]
)
b.body("预期差提示：财务数字（亏损）几乎不影响股价。真正的预期差在于 Apollo 资源量更新时间表 + $5亿 Shelf 使用意图的管理层定性。")
b.page_break()

# ── 【七】核心关注点 ──────────────────────────────────────────────────────────
b.section("【七】本次财报核心关注点")
b.table(
    headers=["优先级", "关注点", "判断标准", "影响"],
    rows=[
        ["1 - 最高", "现金余额与消耗速率",
         "Q1 末现金 > $1.1亿 = 健康；< $1.0亿 + Shelf = 市场质疑资金缺口",
         "高"],
        ["2 - 最高", "Apollo MRE 更新时间表",
         "Q1 报告附带 MRE 预告或初步数字 = 最大正向催化剂",
         "极高"],
        ["3 - 高",   "$5亿 Shelf 定性",
         "战略备用（收购/扩张）= 市场可接受；运营缺口 = 引发抛售",
         "高"],
    ],
    col_widths=[1.0, 1.5, 3.0, 0.8]
)
b.page_break()

# ── 【八】风险提示 ────────────────────────────────────────────────────────────
b.section("【八】风险提示")
b.table(
    headers=["风险类型", "具体风险", "概率", "影响程度"],
    rows=[
        ["稀释风险",   "$5亿 Shelf 相当于市值 32%，若大幅动用将显著摊薄",       "中",    "高"],
        ["钻探风险",   "品位或厚度低于 Apollo 历史截距，直接打击资源量预期",     "低-中", "高"],
        ["金价风险",   "黄金价格大幅回调（$3,200->$2,800），压制勘探股估值",    "低-中", "高"],
        ["地缘风险",   "哥伦比亚政策变化或社区矛盾影响勘探许可续期",             "低",    "极高"],
        ["流动性风险", "日均成交量约 5 万股，机构进出成本高",                    "中",    "中"],
        ["执行风险",   "100,000m 钻探计划因设备/人员问题延迟，影响 MRE 时间表", "低",    "中"],
    ],
    col_widths=[1.0, 3.0, 0.8, 0.9]
)

# ── 附录：情景分析 ────────────────────────────────────────────────────────────
b.section("附录 — 情景分析")
b.table(
    headers=["情景", "核心驱动", "关键数字", "股价预期反应"],
    rows=[
        ["牛市", "MRE 更新披露 + Shelf 定性为战略备用 + 高品位截距持续",
         "现金 > $1.2亿；MRE 吨位上修 > 20%", "+15% ~ +25%"],
        ["基准", "Q1 正常钻探进展，无 MRE 更新，Shelf 解释令市场接受",
         "现金 $1.0~1.2亿；EPS -$0.12 附近",  "+-5%"],
        ["熊市", "Shelf 被解读为资金缺口 + 钻探品位低于预期 + 金价走弱",
         "现金 < $1.0亿；MRE 无更新迹象",      "-15% ~ -20%"],
    ],
    col_widths=[0.8, 2.8, 2.0, 1.1]
)

scenario_chart = cb.scenario_hbar(
    title="Scenario Analysis: Implied Share Price Range",
    scenarios=["Bull Case", "Base Case", "Bear Case"],
    values=[22.56, 18.95, 15.34],
    current=closes[-1],
    current_label=f"${closes[-1]:.2f}",
    colors=["#27AE60", "#1A56DB", "#E74C3C"],
    xlabel="Implied Share Price (USD)",
)
b.image(scenario_chart, width=5.8, caption="情景分析：隐含股价区间 vs 当前价格")

b.disclaimer()
path = b.save()
print(f"已保存：{path}")
