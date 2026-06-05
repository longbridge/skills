# Research: Stock Screeners

覆盖原技能：`longbridge-ark-analysis`, `longbridge-buffett-moat-analyzer`, `longbridge-buffett-moat-stock-screener`, `longbridge-graham-screener`, `longbridge-graham-stock-analysis`, `longbridge-dividend-screen`, `longbridge-value-screen`, `longbridge-factor-screen`, `longbridge-smallcap-growth`

---

## ARK 风格分析（longbridge-ark-analysis）

**触发场景**：_"ARK 风格分析 TSLA"_、_"颠覆性创新诊断"_

**评估四维度**（各25分）：
1. **平台适配性**：是否属于颠覆性技术平台（AI/基因/区块链/能源存储等）
2. **创新收入占比**：核心创新业务营收占比（高占比→纯正颠覆者）
3. **规模经济动态**：产品/服务是否遵循 Wright's Law（成本随累计产量下降）
4. **交叉赋能**：与其他颠覆性平台的协同潜力

---

## 巴菲特护城河分析（longbridge-buffett-moat-analyzer / screener）

**触发场景**：_"AAPL 护城河如何"_、_"用巴菲特眼光看这只股票"_

**五维度护城河评分**（各20分）：
1. **业务与护城河**：品牌/网络效应/成本优势/转换成本/资源壁垒
2. **财务健康**：ROE连续10年>15%/自由现金流正/低负债
3. **管理层诚信**：股东信函分析/薪酬结构/回购vs增发记录
4. **估值**：PE/PB相对历史和行业（巴菲特：合理价买好公司 > 好价买普通公司）
5. **竞争持续性**：护城河是否扩宽中（而非收窄）

**批量筛选**：按上述标准在 A股/港股/美股 中筛选3-5候选

---

## 格雷厄姆价值筛选（longbridge-graham-screener / graham-stock-analysis）

**触发场景**：_"格雷厄姆选股"_、_"净净股"_、_"NCAV 筛选"_

**Net-Net（NCAV）公式**：
```
NCAV = 流动资产 - 总负债
买入标准：股价 < 2/3 × NCAV/股
```

**格雷厄姆七标准**（单股诊断）：
1. PE < 15
2. PB < 1.5
3. PE × PB < 22.5
4. 流动比率 > 2
5. 负债率 < 100%（净负债/净资产）
6. 近10年每股收益无亏损
7. 连续20年股息支付记录

---

## 高股息筛选（longbridge-dividend-screen）

**触发场景**：_"高股息股票"_、_"股息率超过4%的"_

**筛选标准**：股息率 > 3%（可调）+ 近3年连续分红 + 派息率 < 80% + ROE > 10%

---

## 价值投资筛选（longbridge-value-screen）

**触发场景**：_"找被低估的好公司"_、_"基本面强但估值低的股票"_

**筛选标准**（组合使用）：
- ROE > 15% + PE < 行业中位数 + 营收连续增长 + 自由现金流为正

---

## 基本面因子筛选（longbridge-factor-screen）

**触发场景**：按 PE/PB/ROE/营收增速等单一或组合因子筛选。

**支持维度**：PE/PB/PS/ROE/净利润增速/营收增速/自由现金流率/负债率

---

## 小盘成长股筛选（longbridge-smallcap-growth）

**触发场景**：_"找专精特新小盘股"_、_"港股小盘成长"_

**筛选标准**：市值<50亿（A股）或<100亿港元 + 营收增速>30% + 技术护城河/研发强度高
