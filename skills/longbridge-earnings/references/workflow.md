# Detailed Workflow for Earnings Updates

This document provides detailed step-by-step instructions for each phase of the earnings update process.

## Contents

- [Phase 1: Earnings Data Collection](#phase-1-earnings-data-collection) — Steps 1–4
  - Step 1: Identify the latest earnings period
  - Step 2: Gather earnings materials (filings, transcripts, press release)
  - Step 3: Extract key metrics
  - Step 4: Identify key themes from the call
- [Phase 2: Analysis](#phase-2-analysis) — Steps 5–11
  - Step 5: Beat / miss analysis
  - Step 6: Segment / geographic / product analysis
  - Step 7: Margin analysis
  - Step 8: Guidance analysis
  - Step 9: Update financial model
  - Step 10: Update valuation & price target
  - Step 11: Assess rating impact
- [Phase 3: Chart Generation](#phase-3-chart-generation) — Step 12
- [Phase 4: Report Creation](#phase-4-report-creation) — Steps 13–14
- [Phase 5: Quality Check & Delivery](#phase-5-quality-check--delivery) — Steps 15–16
- [Phase 6: Conversation Summary](#phase-6-conversation-summary) — Step 17

## ⚠️ CRITICAL: USE LONGBRIDGE CLI TO IDENTIFY THE LATEST EARNINGS ⚠️

Training data is OUTDATED. Always use `longbridge filing` to find and verify the latest earnings quarter. Do NOT rely on knowledge cutoff or web search as the primary method.

## Phase 1: Earnings Data Collection

### Step 1: Identify the Latest Earnings Period

**Use longbridge CLI as the primary method** to detect the latest reported quarter:

Run `longbridge filing --help` to see available options. List recent filings and filter for the latest 10-Q (quarterly) or 10-K (annual) by date. Note the filing ID, then use filing detail to read the header and extract the period end date (e.g., "For the quarterly period ended [DATE]").

**Step 1c: Map period-end date to fiscal quarter**

Use the company's fiscal calendar to convert the period-end date:
- **Calendar year** (most companies): Q1=Jan-Mar, Q2=Apr-Jun, Q3=Jul-Sep, Q4=Oct-Dec
- **Non-standard fiscal year**: Check the filing header or search `[company] fiscal year calendar`
  - Apple: FY ends Sep → Q1=Oct-Dec, Q2=Jan-Mar, Q3=Apr-Jun, Q4=Jul-Sep
  - Nike: FY ends May → Q1=Jun-Aug, Q2=Sep-Nov, Q3=Dec-Feb, Q4=Mar-May
  - Walmart: FY ends Jan → Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan

**Step 1d: Verify the filing is recent**

Check that the filing's publication date is within the last 3 months from today. If older:
- The company may not have reported yet for the current quarter
- Inform the user which quarter is the latest available

**If no 10-Q/10-K found** (non-US companies, new listings):
- Use `longbridge news --help` to search for earnings-related news
- As a last resort, ask the user to specify the quarter

**⚠️ HK/CN symbol format note**: Leading zeros in HK symbols can cause empty results. If `09988.HK` returns no data, try `9988.HK`. Always verify with `longbridge filing --help` examples.

**Step 1b: Understand Company's Fiscal Calendar**

After identifying the latest quarter, understand the company's fiscal year to interpret it correctly:

**Common fiscal year patterns:**
- **Calendar year (CY)**: Q1=Jan-Mar, Q2=Apr-Jun, Q3=Jul-Sep, Q4=Oct-Dec
- **Nike fiscal**: Q1=Jun-Aug, Q2=Sep-Nov, Q3=Dec-Feb, Q4=Mar-May (May fiscal year-end)
- **Apple fiscal**: Q1=Oct-Dec, Q2=Jan-Mar, Q3=Apr-Jun, Q4=Jul-Sep (September fiscal year-end)
- **Walmart fiscal**: Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan (January fiscal year-end)

Many companies state their fiscal year in the earnings release header. Search `[company] fiscal year calendar` if needed.

**MANDATORY VERIFICATION before proceeding:**

- [ ] Used `longbridge filing` to find the latest 10-Q/10-K (NOT web search or training data)
- [ ] Read the filing header via `longbridge filing detail` to extract "period ended [DATE]"
- [ ] Mapped the period-end date to the correct fiscal quarter using company's fiscal calendar
- [ ] Filing publication date is within 3 months of today
- [ ] Confirmed quarter with the user (if auto-detected)

### Step 2: Gather Earnings Materials

After confirming the quarter (Step 1), collect materials **primarily via longbridge CLI**:

**Primary Materials (REQUIRED) — use longbridge CLI first:**

- **Financial statements** — use `longbridge financial-report --help` to get structured income statement, balance sheet, and cash flow data. This is the **primary source for financial figures** (especially for HK/CN stocks where filing PDFs are not machine-readable).
  - Query each statement kind separately (`--kind IS`, `--kind BS`, `--kind CF`) — `--kind ALL` may return empty for some symbols.
  - If a symbol returns empty, try dropping leading zeros: `09988.HK` → `9988.HK`, `00700.HK` → `700.HK`.

- **10-Q or 10-K filing** (for US stocks, already identified in Step 1):
  Use `longbridge filing --help` to access filing detail — contains full financial statements, MD&A, and risk factors. For Q4 use the 10-K (annual); for Q1-Q3 use the 10-Q.
  - **Note**: HK/CN filings are typically PDF — `longbridge filing detail` will return an "unsupported format" error. Use `longbridge financial-report` instead for structured data.

- **Earnings press release / 8-K** — often filed as 8-K on the same day:
  Use `longbridge filing --help` to list and filter for 8-K filings near the same date as the 10-Q. The 8-K often contains the earnings press release as an exhibit.

- **Earnings-related news** via longbridge:
  Use `longbridge news --help` to search for earnings-related news. Look for titles containing "earnings", "results", "revenue", "Q[X]". Read full articles for analyst commentary and consensus data.

- **Earnings call transcript** — NOT available via longbridge, use web search:
  - Search: "[Company] Q[X] [Year] earnings call transcript"
  - Verify the transcript date matches the filing date from Step 1

**Supplemental Materials (if available):**
- **Investor presentation/slides** - Often posted on IR site alongside press release
- **Supplemental data file** - Some companies provide Excel files with detailed metrics

**Reference Materials (for comparison):**
- **Prior quarter results** - For QoQ comparison (90 days ago)
- **Prior year same quarter** - For YoY comparison (4 quarters ago)
- **Prior estimates** - If this company was previously covered
- **Consensus estimates** - Via web search (not available in longbridge CLI)
  - CRITICAL: Use estimates from BEFORE earnings release
  - Needed for beat/miss analysis

**🛑 MANDATORY VERIFICATION before proceeding to Step 3:**

**DATES - Verify ALL dates match:**
- [ ] ✅ **Today's date written down**: _______________
- [ ] ✅ **Earnings release date**: _______________ (MUST be within 3 months of today)
- [ ] ✅ **Earnings call transcript date**: _______________ (MUST match release date ±1 day)
- [ ] ✅ **10-Q/10-K filing date**: _______________ (MUST be same quarter as release)
- [ ] ✅ **ALL materials show SAME quarter** (e.g., all say "Q3 2024", not mixed quarters)

**SEARCH & ACCESS - Verify active search completed:**
- [ ] ✅ **SEARCHED** for "latest earnings" (not assumed based on current date)
- [ ] ✅ **ACCESSED** actual earnings press release and read it
- [ ] ✅ **OPENED** actual earnings call transcript and verified date
- [ ] ✅ **CONFIRMED** this is the MOST RECENT quarter by checking dates
- [ ] ✅ Have full financial results (revenue, EPS, margins, etc.) from actual release
- [ ] ✅ Have pre-earnings consensus estimates with source date

**🚨 RED FLAGS - STOP if ANY of these are true:**
- 🚨 Did NOT actually search for or access the earnings materials
- 🚨 Working from memory or training data instead of current documents
- 🚨 The earnings release date is more than 90 days old
- 🚨 Cannot state the EXACT DATE of the earnings release
- 🚨 The transcript date does NOT match the release date
- 🚨 Materials show different quarters (e.g., release says Q3 but transcript says Q2)
- 🚨 Grabbed the first result without verifying the date

### Step 3: Extract Key Metrics

Create a structured summary:

```
REPORTED RESULTS vs. ESTIMATES:
─────────────────────────────────────────────────
                    Reported    Our Est    Consensus    Beat/(Miss)
Revenue             $X,XXX      $X,XXX     $X,XXX       $XX (X%)
Gross Margin        XX.X%       XX.X%      XX.X%        XXbps
EBITDA              $XXX        $XXX       $XXX         $XX (X%)
Operating Profit    $XXX        $XXX       $XXX         $XX (X%)
EPS (Adjusted)      $X.XX       $X.XX      $X.XX        $X.XX
EPS (GAAP)          $X.XX       $X.XX      $X.XX        $X.XX

KEY BUSINESS METRICS:
─────────────────────────────────────────────────
[Metric 1]          XXX         XXX        XXX          +X% YoY
[Metric 2]          XXX         XXX        XXX          +X% YoY
[Metric 3]          XXX         XXX        XXX          +X% YoY
```

### Step 4: Identify Key Themes from Call

Listen to or read earnings call transcript and note:
- Management's tone (confident, cautious, defensive?)
- Key topics emphasized (product launches, geographic trends, competition)
- Questions from analysts (what are investors concerned about?)
- Guidance provided (raised, lowered, maintained, introduced?)
- Any surprises or unexpected commentary

## Phase 2: Analysis

### Step 5: Beat/Miss Analysis

For EACH key metric that beat or missed, explain:

**If BEAT:**
- What drove the outperformance?
- Was it one-time or sustainable?
- Did management guide higher going forward?
- How does this impact our thesis?

**If MISS:**
- What went wrong?
- Was it company-specific or industry-wide?
- Is management taking corrective action?
- How does this impact our thesis?

**Example Format:**
```
■ **Revenue Beat by 3% Driven by Strong DTC Performance**

Revenue of $13.5B exceeded our estimate of $13.1B by $400M (3%) and consensus
of $13.2B by $300M (2%). The outperformance was driven primarily by Direct-to-
Consumer channels, which grew 18% YoY (vs. our 12% estimate), offsetting
weaker-than-expected wholesale (-5% vs. flat estimate). Management cited strong
digital demand and successful product launches as key drivers. DTC now represents
42% of total revenue vs. 38% a year ago, demonstrating successful channel shift.
```

### Step 6: Segment/Geographic/Product Analysis

Analyze performance by:
- Business segment (if multi-segment company)
- Geography (North America, Europe, China, etc.)
- Product category
- Channel (retail, wholesale, e-commerce)

Identify:
- What outperformed expectations?
- What underperformed?
- Trends vs. prior quarters
- Management commentary on outlook for each area

### Step 7: Margin Analysis

Analyze profitability:
- Gross margin: up or down? why?
- Operating margin: up or down? why?
- Key drivers (pricing, mix, costs, leverage)
- Outlook going forward

### Step 8: Guidance Analysis

If company provided guidance:
- Compare new guidance to prior guidance
- Compare to internal estimates and Street estimates
- Assess credibility (does company have track record of sandbagging? beating?)
- Identify key assumptions behind guidance

If company did NOT provide guidance:
- Note this explicitly
- Provide independent outlook based on results and commentary

### Step 9: Update Financial Model

Update estimates for:
- Current year (remaining quarters)
- Next year
- Potentially year after

**Show clearly:**
```
UPDATED ESTIMATES:
─────────────────────────────────────────────────
                        Old Est     New Est     Change      Reason
FY2024E Revenue         $XX.XB      $XX.XB      +X.X%      [Brief reason]
FY2024E EBITDA          $X.XB       $X.XB       +X.X%      [Brief reason]
FY2024E EPS             $X.XX       $X.XX       +X.X%      [Brief reason]

FY2025E Revenue         $XX.XB      $XX.XB      +X.X%      [Brief reason]
FY2025E EBITDA          $X.XB       $X.XB       +X.X%      [Brief reason]
FY2025E EPS             $X.XX       $X.XX       +X.X%      [Brief reason]
```

### Step 10: Update Valuation & Price Target

**See [valuation-methodologies.md](valuation-methodologies.md) for complete formulas and [report-structure.md](report-structure.md) PAGES 8-10 for output format.**

Use `longbridge calc-index --help`, `longbridge static --help`, `longbridge kline --help`, and `longbridge filing --help` to fetch the market and financial data needed for valuation.

**Three methods with DYNAMIC weighting:**
1. **DCF (40-60%)** — 8-step process: WACC from beta + CAPM, FCF projections, terminal value. Higher weight when forecast confidence is high.
2. **Trading Comps (25-40%)** — Peer median P/E and EV/EBITDA. Higher weight for mature/stable companies in normal markets.
3. **Precedent Transactions (0-25%)** — Only include when M&A data is available and relevant. Use web search for deal data.

**State your chosen weights and explain why.**

**Output: Bear/Base/Bull valuation range**, not a single number:
- **Bear**: Conservative growth, WACC +50bps, 25th percentile peer multiples
- **Base**: Most likely scenario from updated Q[X] estimates
- **Bull**: Optimistic growth, WACC -50bps, 75th percentile peer multiples

**Price target = Base Case weighted average.** Show ALL math.

**Sanity checks:**
- DCF implied price within ±30% of market price
- All methods directionally agree
- Terminal value = 50-70% of total EV
- Historical multiples: current vs. company's own history

**Price Target Decision:**
- If estimates changed significantly (>5%) → Usually change price target
- If estimates changed marginally (<5%) → May maintain price target
- If thesis strengthened/weakened → May change even without estimate change

### Step 11: Assess Rating Impact

Decide whether to change rating:
- If results significantly better than expected + guidance raised → Consider upgrade
- If results significantly worse + guidance cut → Consider downgrade
- If inline or mixed → Usually maintain rating

**Consider:**
- Stock reaction (up/down/flat?)
- Valuation (expensive/cheap relative to new estimates?)
- Risk/reward (asymmetry shifted?)

## Phase 3: Chart Generation

### Step 12: Generate 8-12 Charts

Create charts focusing on QUARTERLY TRENDS and WHAT'S NEW.

**REQUIRED CHARTS (8-12 total):**

1. **Quarterly Revenue Progression** (Bar chart) — last 8-12 quarters, highlight beat/miss
2. **Quarterly EPS Progression** (Bar chart) — adjusted and GAAP, last 8-12 quarters
3. **Quarterly Margin Trend** (Line chart) — gross, EBIT, net margin trajectory
4. **Revenue by Segment/Geography** (Stacked bar) — current quarter vs. YoY
5. **Key Operating Metrics** (Multi-line) — customer count, ARPU, units, etc.
6. **Beat/Miss Summary** (Waterfall or table) — components of variance from estimates
7. **Estimate Revision Chart** (Before/after) — old vs. new FY estimates
8. **Valuation Chart** (P/E or EV/EBITDA) — historical multiple range vs. current

**OPTIONAL CHARTS (if space allows):**
- Peer comparison, guidance vs. Street, cash flow metrics

**Chart Style Guidelines:**
- Focus on TRENDS (quarterly progression)
- Highlight CHANGES (beat/miss, estimate revisions)
- Keep simple and clear (fast-turnaround report)

## Phase 4: Report Creation

### Step 13: Create DOCX Report

Use the template at `scripts/generate_report.py` as a starting point. Fill in the DATA SECTION with actual company data and run it. The template handles CJK/Latin bilingual fonts and embeds charts via `BytesIO` (no PNG files saved to disk).

See [report-structure.md](report-structure.md) for complete page-by-page templates and formatting requirements.

**Key Steps:**
1. Create Page 1 with earnings summary and quick takeaways
2. Add detailed results analysis (Pages 2-3)
3. Include key metrics and guidance (Pages 4-5)
4. Update investment thesis (Pages 6-7)
5. Provide valuation and estimates (Pages 8-10)
6. Add appendix if needed (Pages 11-12)
7. Embed all 8-12 charts throughout
8. Add 1-3 summary tables
9. Include complete sources section with clickable hyperlinks

### Step 14: Optional - Update XLS Model

If a full financial model exists for this company (from initiation), update it with:
- Actual Q[X] results
- Revised estimates for future quarters
- Updated valuation

**Note**: For earnings updates, a full XLS file is OPTIONAL. The DOCX report is the primary deliverable.

## Phase 5: Quality Check & Delivery

### Step 15: Quality Checklist

Before publishing, verify:

**Content:**
- [ ] Beat/miss clearly stated and quantified
- [ ] Key drivers explained (not just "strong performance")
- [ ] Updated estimates provided (old vs. new shown)
- [ ] Price target updated or explicitly maintained
- [ ] Rating confirmed or changed with rationale
- [ ] Guidance analyzed (if provided)
- [ ] Thesis impact assessed

**Formatting:**
- [ ] Page 1 has summary box and key bullets
- [ ] All tables have source lines
- [ ] All figures numbered and captioned
- [ ] Estimates table shows old vs. new
- [ ] 8-12 charts embedded throughout
- [ ] Report is 8-12 pages

**Citations:** ⭐ MANDATORY
- [ ] Every figure has specific source with document and date
- [ ] Every table has specific source with document reference
- [ ] Beat/miss analysis cites consensus source with date
- [ ] Sources section lists all materials with URLs
- [ ] ALL URLs are CLICKABLE HYPERLINKS (not plain text)
- [ ] All SEC filings hyperlinked (use `longbridge filing` to find filing URLs)
- [ ] Earnings call quotes cite specific speaker and approximate timestamp

**Timeliness:**
- [ ] Report published within 24-48 hours of earnings release
- [ ] All data is from LATEST quarter
- [ ] Consensus estimates are pre-earnings (not post-earnings)

### Step 16: Deliver Report

Provide user with:

1. **DOCX file**: `[Company]_Q[X]_[Year]_Earnings_Update.docx`
2. **Optional XLS**: Updated financial model if maintained

**Brief summary for user:**
```
[Company] Q[X] [Year] Earnings Update Complete

Results: [BEAT / INLINE / MISS]
- Revenue: $X.XB ([beat/missed] by $XXM or X%)
- EPS: $X.XX ([beat/missed] by $X.XX)

Key Takeaways:
■ [Takeaway 1]
■ [Takeaway 2]
■ [Takeaway 3]

Updated Estimates:
- FY[Year]E Revenue: $XX.XB (prior: $XX.XB, [+/-]X%)
- FY[Year]E EPS: $X.XX (prior: $X.XX, [+/-]X%)

Rating: [MAINTAINED / RAISED / LOWERED] [RATING]
Price Target: $XXX (prior: $XXX) - [+/-]XX% upside
```

---

## Phase 6: Conversation Summary

After delivering the DOCX report, output a structured summary **directly in the conversation** using markdown tables and Unicode formatting.

**See [summary-card-spec.md](summary-card-spec.md) for the complete output format.**

### Step 17: Extract Data & Output Summary

From the completed report, extract and output the following 8 modules. **Do NOT fabricate data — skip any module with missing data.**

**Module 1 — Header:**
```
**[Company] ([Ticker])** — [Quarter] [Year] Earnings Update
🟢 Buy  |  Target: $XXX  |  Current: $XXX  |  Upside: +XX%
```

**Module 2 — Core KPI Table** (4-5 key metrics):

| Metric | Reported | YoY | vs Estimate |
|--------|----------|-----|-------------|
| Revenue | ... | +XX% | Beat +X% |

**Module 3 — Revenue by Segment** (with Unicode █ bars):

| Segment | Revenue | Share | YoY |
|---------|---------|-------|-----|
| Gaming | RMB 53B | ████████████ 33% | +12% |

**Module 4 — Quarterly Revenue Trend** (last 6-8 quarters):

| Q2'25 | Q3'25 | Q4'25 | Q1'26 |
|-------|-------|-------|-------|
| 180.3 | 185.1 | 190.0 | 198.9 |

**Module 5 — Investment Thesis** (status tags + one-line summary):
- 🟢 Strengthened / 🟡 Maintained / 🟠 Weakened / 🔵 New Focus

**Module 6 — Price Target** (methods, weights, comps):

| Method | Weight | Parameter | Result |
|--------|--------|-----------|--------|
| P/E | 70% | EPS × 25x | $XXX |

**Module 7 — Estimate Revisions** (old→new + forward years):

| Metric | FY26E (Old) | FY26E (New) | Chg | FY27E |
|--------|-------------|-------------|-----|-------|

**Module 8 — Key Risks** (inline backtick tags):
```
Risks: `Tag1` · `Tag2` · `Tag3` · `Tag4` · `Tag5`
```