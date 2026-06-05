# Research: Reports and Investment Ideas

覆盖原技能：`longbridge-coverage-initiation`, `longbridge-investment-proposal`, `longbridge-investment-ideas`

---

## longbridge-coverage-initiation — 首次覆盖报告

**触发场景**：生成机构级首次覆盖研究报告（8-12页 DOCX）。

**报告框架**（5步工作流）：

1. **公司介绍**：业务模式/市场定位/竞争优势
2. **行业与竞争格局**：TAM/竞争对手/护城河分析
3. **财务分析**：历史3-5年财务走势 + 未来2-3年预测
4. **估值**：多种方法（DCF/PE Band/EV-EBITDA）+ 目标价
5. **投资结论**：评级（买入/持有/卖出） + 主要催化剂 + 关键风险

**DOCX 生成**：如 `scripts/` 目录下有 DOCX 生成脚本，调用它；否则输出 Markdown 结构

---

## longbridge-investment-proposal — 投资备忘录

**触发场景**：为特定标的生成结构化投资备忘录（含入场/出场/止损逻辑）。

**备忘录结构**：
```
投资备忘录：{symbol}
日期：{YYYY-MM-DD}

投资逻辑（Bull Case）：
- {核心论点1}
- {核心论点2}

风险因素（Bear Case）：
- {主要风险1}
- {主要风险2}

入场区间：${X} - ${Y}（基于估值支撑/技术支撑）
目标价：${X}（{方法论}，预期回报 {X}%）
止损：${X}（理由）
持有周期：{X} 个月/年

量化标准：{可验证的信号，如 EPS 修订/营收增速/管理层指引}

⚠️ 以上内容仅供参考，不构成投资建议。
```

---

## longbridge-investment-ideas — 投资机会生成

**触发场景**：系统性发掘新的投资机会（结合量化筛选+定性分析）。

**生成框架**：
1. **量化筛选**：用 `longbridge-research` 各类 screener 按条件过滤
2. **宏观/行业主题**：识别当前市场主线（AI/新能源/消费复苏等）
3. **催化剂识别**：即将发生的事件（财报/政策/产品发布）
4. **初步筛选结果**：3-5个候选标的 + 投资逻辑摘要

**输出格式**：
- 市场主题识别 → 受益行业/板块
- 3-5只候选标的（附简短投资逻辑）
- 建议下一步深度研究的标的
