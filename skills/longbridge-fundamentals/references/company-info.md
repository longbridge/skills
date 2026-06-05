# Fundamentals: Company Information

覆盖原技能：`longbridge-basicinfo`, `longbridge-company-profile`, `longbridge-company-tearsheet`, `longbridge-corporate`

---

## longbridge-basicinfo — 证券静态基本信息

**触发场景**：上市日期/交易所/股本/手数/EPS/BPS/股息率等静态参考数据。

**数据类型**：
- 公司名（中/英）、上市日期、交易所、行业分类
- 总股本/流通股本/限售股本
- 每手股数（lot size）、EPS（基本/摊薄）、BPS、股息率
- 货币、面值

**工作流**：`longbridge <basicinfo-subcommand> SYMBOL --format json`

---

## longbridge-company-profile — 公司介绍（Pitch-book 格式）

**触发场景**：生成机构风格的公司介绍页，用于客户材料或研究开篇。

**输出内容**：
- 公司概述（一段话业务描述）
- 主营业务架构（分部/产品线）
- 竞争优势与护城河（2-3点）
- 财务概览（最新年度营收/净利润/市值）
- 管理层（CEO/CFO）
- 近期大事件

**工作流**：
1. 获取 basicinfo + 最新财务 KPI（参考 core-data.md）
2. 结合 WebSearch 获取业务描述（标注来源）
3. 输出 pitch-book 格式

---

## longbridge-company-tearsheet — 公司一页纸快照

**触发场景**：生成高密度的公司一页纸（tear sheet），涵盖价格/估值/财务/评级。

**输出内容**：
- 头部：价格/涨跌幅/52周高低/市值
- 估值：PE/PB/PS/EV-EBITDA
- 财务：最新年度营收/净利润/自由现金流/ROE
- 增长：YoY 营收增速/EPS 增速
- 分析师：共识评级/目标价
- 近期新闻：1-3条最新标题

**工作流**：并行获取报价、基本面、估值、研报数据；合并为紧凑格式

---

## longbridge-corporate — 公司法律与股权结构

**触发场景**：公司法律结构/控股架构/VIE 结构/实际控制人查询。

**数据类型**：
- 公司法律架构（持股结构图描述）
- VIE 结构（如适用）
- 实际控制人/最终受益人

**工作流**：`longbridge <corporate-subcommand> SYMBOL --format json`；结合 SEC 或港交所公告补充细节。
