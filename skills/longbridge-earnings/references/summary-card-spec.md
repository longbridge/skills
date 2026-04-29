# Conversation Summary Format

After generating the DOCX report, output a structured summary **directly in the conversation** using markdown tables and Unicode formatting. This replaces the need for a separate file — the user can see all key data at a glance.

## Data Extraction Rules

Extract the following 8 modules from the report. **If a module's data is missing, skip it — do NOT fabricate.**

---

## Output Format

### Module 1: Header

```
**[Company Name] ([Ticker])** — [Quarter] [Year] Earnings Update
Rating: [RATING]  |  Target: $XXX  |  Current: $XXX  |  Upside: +XX%
Report Date: YYYY-MM-DD
```

Use bold for company name. Rating with emoji indicator:
- Buy/Outperform → 🟢
- Neutral/Hold → 🟡
- Underperform/Sell → 🔴

### Module 2: Core KPI Table

Markdown table with 4-5 key metrics:

```
| Metric | Reported | YoY | vs Estimate |
|--------|----------|-----|-------------|
| Revenue | RMB XX.XB | +XX% | Beat +X.X% |
| Net Income | RMB XX.XB | +XX% | Beat +X.X% |
| Non-GAAP NI | RMB XX.XB | +XX% | Beat +X.X% |
| Gross Margin | XX.X% | +XXbps | Beat +XXbps |
| EPS | $X.XX | +XX% | Beat +X.X% |
```

Prefix beat/miss with directional text: "Beat +X%" or "Miss -X%".

### Module 3: Revenue by Segment

```
| Segment | Revenue | Share | YoY |
|---------|---------|-------|-----|
| [Segment A] | RMB XX.XB | XX% | +XX% |
| [Segment B] | RMB XX.XB | XX% | +XX% |
| [Segment C] | RMB XX.XB | XX% | +XX% |
```

Use Unicode bar to visualize share:

```
| Segment | Revenue | Share | YoY |
|---------|---------|-------|-----|
| Gaming | RMB 53.2B | ████████████ 33% | +12% |
| FinTech | RMB 48.1B | ██████████ 30% | +8% |
| Ads | RMB 30.5B | ██████ 19% | +18% |
| Cloud | RMB 18.2B | ████ 11% | +35% |
| Other | RMB 11.0B | ██ 7% | +5% |
```

Bar width proportional to share percentage: 1 block (█) per ~3%.

### Module 4: Quarterly Revenue Trend

Unicode sparkline or simple table:

```
Quarterly Revenue Trend (RMB B):
Q2'24  Q3'24  Q4'24  Q1'25  Q2'25  Q3'25  Q4'25  Q1'26
161.1  167.2  172.4  175.0  180.3  185.1  190.0  198.9
       ▁▂▃▄▅▆▇ ↗ trending up
```

Or as a compact table if the sparkline characters don't render well:

```
| Q2'24 | Q3'24 | Q4'24 | Q1'25 | Q2'25 | Q3'25 | Q4'25 | Q1'26 |
|-------|-------|-------|-------|-------|-------|-------|-------|
| 161.1 | 167.2 | 172.4 | 175.0 | 180.3 | 185.1 | 190.0 | 198.9 |
```

### Module 5: Investment Thesis

Bulleted list with status tags:

```
Investment Thesis:

■ [🟢 Strengthened] **AI monetization accelerating**
  Cloud revenue grew 35% YoY with 3 price hikes in 2026, validating AI spend.

■ [🟡 Maintained] **Gaming portfolio remains resilient**
  Delta Force and Honor of Kings performing well, but regulatory uncertainty persists.

■ [🟠 Weakened] **Margin expansion story under pressure**
  AI capex doubling to >RMB 36B creates near-term compression risk.

■ [🔵 New Focus] **WeChat AI ecosystem emerging**
  OpenClaw agents and WeChat AI search creating new monetization surface.
```

Status tag colors (text representation):
- 🟢 Strengthened / 显著强化
- 🟡 Maintained / 稳定维持
- 🟠 Weakened / 有所弱化
- 🔵 New Focus / 新增关注

### Module 6: Price Target Derivation

```
Price Target: $XXX (+XX% upside)

| Method | Weight | Key Parameter | Result |
|--------|--------|---------------|--------|
| P/E | 70% | FY26E EPS $X.XX × 25x | $XXX |
| DCF | 30% | WACC X.X%, TGR 2.5% | $XXX |
| **Blended** | **100%** | | **$XXX** |

Current P/E: XX.Xx vs Historical Avg: XX.Xx
⚠️ [Warning if current > 1.3× historical: "Valuation elevated — current XX.Xx vs historical avg XX.Xx"]

Comparable Companies:
| Company | P/E | EV/EBITDA |
|---------|-----|-----------|
| [Peer 1] | XX.Xx | XX.Xx |
| [Peer 2] | XX.Xx | XX.Xx |
| [Peer 3] | XX.Xx | XX.Xx |
```

### Module 7: Estimate Revisions

```
| Metric | FY26E (Old) | FY26E (New) | Chg | FY27E | FY28E |
|--------|-------------|-------------|-----|-------|-------|
| Revenue | $XX.XB | $XX.XB | +X% | $XX.XB | $XX.XB |
| Net Income | $X.XB | $X.XB | +X% | $X.XB | $X.XB |
| EPS | $X.XX | $X.XX | +X% | $X.XX | $X.XX |
| P/E | XX.Xx | XX.Xx | | XX.Xx | XX.Xx |
```

If P/E > 1.3× historical average, append ⚠️ to that cell.

### Module 8: Key Risks

Inline tags on one line:

```
Risks: `Macro Slowdown` · `AI Margin Compression` · `FX Headwind` · `Regulatory Risk` · `Valuation Premium` · `Competition`
```

Use backtick formatting for each risk tag, separated by ` · `.

---

## Complete Example Output

```
**Tencent (00700.HK)** — Q1 2026 Earnings Update
🟢 Buy  |  Target: HK$722  |  Current: HK$479  |  Upside: +50.7%
Report Date: 2026-04-29

| Metric | Reported | YoY | vs Estimate |
|--------|----------|-----|-------------|
| Revenue | RMB 198.9B | +13.7% | Beat +2.1% |
| Non-IFRS NI | RMB 56.5B | +18.2% | Beat +3.4% |
| Gross Margin | 53.2% | +180bps | Beat +90bps |
| EPS | HK$8.29 | +19.1% | Beat +3.8% |

| Segment | Revenue | Share | YoY |
|---------|---------|-------|-----|
| Gaming | RMB 53.2B | ████████████ 33% | +12% |
| FinTech | RMB 48.1B | ██████████ 30% | +8% |
| Advertising | RMB 30.5B | ██████ 19% | +18% |
| Cloud | RMB 18.2B | ████ 11% | +35% |

Quarterly Revenue (RMB B):
| Q2'25 | Q3'25 | Q4'25 | Q1'26 |
|-------|-------|-------|-------|
| 180.3 | 185.1 | 190.0 | 198.9 |

Investment Thesis:

■ [🟢 Strengthened] **AI monetization accelerating**
  Cloud revenue grew 35% with 3 price hikes in 2026.

■ [🟡 Maintained] **Gaming resilient**
  Delta Force + Honor of Kings solid, regulatory risk lingers.

■ [🟠 Weakened] **Margin expansion pressured**
  AI capex >RMB 36B creates near-term compression.

Price Target: HK$722 (+50.7% upside)

| Method | Weight | Parameter | Result |
|--------|--------|-----------|--------|
| P/E | 70% | FY26E EPS HK$8.29 × 25x | HK$707 |
| DCF | 30% | WACC 9.2%, TGR 3% | HK$756 |
| **Blended** | **100%** | | **HK$722** |

Current P/E: 17.6x vs Historical Avg: 25x — undervalued

| Peer | P/E |
|------|-----|
| Alibaba (09988.HK) | 12.3x |
| Meituan (03690.HK) | 22.1x |
| NetEase (09999.HK) | 15.8x |

| Metric | FY26E (Old) | FY26E (New) | Chg | FY27E |
|--------|-------------|-------------|-----|-------|
| Revenue | RMB 780B | RMB 795B | +1.9% | RMB 890B |
| Net Income | RMB 215B | RMB 225B | +4.7% | RMB 260B |
| EPS | HK$32.10 | HK$33.60 | +4.7% | HK$38.80 |
| P/E | 14.9x | 14.3x | | 12.4x |

Risks: `AI Margin Compression` · `Macro Weakness` · `U.S. Regulatory` · `Gaming Tax` · `FX Headwind` · `Valuation Risk`
```

## Guidelines

- Keep the entire summary compact — aim for one screenful if possible
- Use markdown tables for structured data (renders well in terminal)
- Use Unicode block chars (█) for segment share bars
- Use emoji for status indicators (🟢🟡🟠🔴🔵⚠️)
- All numbers must come from the DOCX report — never fabricate
- If a module has no data, skip it silently
- **DO NOT output a Sources section or any reference links in the conversation.** All citations and hyperlinks belong in the DOCX only. Suppress any auto-generated sources footer.
