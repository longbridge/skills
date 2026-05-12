# Output Template

## Instructions

This file defines the output structure for the Financial Calendar Skill. Each output consists of four sections, each corresponding to a template. A section is generated if data exists, or omitted if not (but Section 1 must always be included). The four sections are concatenated in order to form a complete report, with disclaimer text appended once at the very end.

**Core Principles:**
- **Focus on the future.** Only output events that have not yet occurred. The sole exception: earnings results released last night/pre-market today may be briefly mentioned in Sections 1 and 3. Earlier historical events are never included.
- **Generate as much as possible.** Output as many future events as there are — do not artificially truncate. Every holding and watchlist security with events must be covered. High-attention market-wide events should also be selectively included.
- **No duplication.** The same event appears only once and is not repeated across sections.

Security identifier format varies by context:

- **When on its own line** (e.g., event list title line): `[Company Name] [Code] · [Market] · [Holdings / Watchlist / Market]`
- **When embedded in a sentence** (e.g., portfolio linkage, impact description, inline references): `[Company Name] ([Code] · [Market] · [Holdings / Watchlist])`, wrapped in parentheses for readability

Three source tags:
- **Holdings** — Securities currently held by the user
- **Watchlist** — Securities in the user's watchlist
- **Market** — Neither holdings nor watchlist, but a high-attention market-wide event (marquee earnings, hot IPOs, industry leaders, etc.) included to help users discover opportunities

Examples:

- SMIC 688981 · A-shares · Holdings
- SMIC 0981.HK · HK · Watchlist
- NVIDIA NVDA · US · Watchlist
- Pinduoduo PDD · US · Market (not held/watchlisted by user, but a major earnings report)
- [Company] · HK · Market · IPO (hot new listing)

Time format: Beijing Time (CST), with original timezone noted in parentheses

Example: 08:30 CST (20:30 ET previous day)

---

## Section 1: Event Overview (Template 1)

The core section of the report. All events (macro, holdings, watchlist, high-attention market-wide events) are merged onto a single timeline, sorted uniformly by time.

```text
📅 [Month Day (to Month Day)] Financial Calendar Brief

> [One-line summary of key highlights, e.g., "This week is packed with inflation data, plus several Chinese ADR earnings"]

━━ Last Night / Pre-Market Results ━━
[Company Name] [Code] · [Market] Earnings Released
Actual EPS: [X.XX] vs Expected [X.XX] ([+/-X%])
Key Highlight: [One sentence — the most critical business metric]
→ Portfolio Linkage: [Stock Name] [Code] · [Market] · [Holdings/Watchlist] — [Impact direction] (if the earnings security itself is not holdings/watchlist, explain why it's worth noting)

[More released results...]

━━ Upcoming ━━

[Month Day (Weekday)]

[Company Name] [Code] · [Market] · [Holdings/Watchlist/Market]
  · [Event Type] · [HH:MM CST] ([Original Timezone]) — [One-line impact description]
  · [Event Type] · [HH:MM CST] — [One-line impact description]
  Cross-Market: [If likely to move other securities, briefly explain]
  💡 Why Watch: [Only for "Market" tagged securities — one sentence explaining why this event is worth attention]

[Macro Event Name] · [HH:MM CST] ([Original Timezone]) · Importance [★ count]
  [One sentence explaining what this event is]
  Portfolio Linkage: [Impact direction, which securities are involved; inline references use parenthetical format e.g., "Microsoft (MSFT · US · Holdings)"]

[Company Name] [Code] · [Market] · [Holdings/Watchlist/Market]
  · [Event Type] · [HH:MM CST] — [One-line impact description]

[Month Day (Weekday)]

[Continue in chronological order...]
```

Field Rules:

| Field | Rule |
| ---- | ---- |
| Last Night / Pre-Market Results | Limited to earnings released between the previous trading day's close and today's open. Earlier history is not included. Omit entire block if none |
| Date Grouping | Group by calendar day, one date heading per day (e.g., "May 12 (Monday)"), sorted chronologically within each day |
| Security Events | Tag each security with "Holdings", "Watchlist", or "Market". "Market" securities require a "Why Watch" explanation. Securities with no events do not appear. "Market" securities emerge naturally from unfiltered market-wide data; no hard quantity requirement |
| Macro Events | Interleaved with security events on the same timeline, not grouped separately. Marked with importance star rating |
| Cross-Market | Only included when an event may move other holdings/watchlist securities. State direction only, no magnitude prediction. Omit if no cross-market impact |
| Event Type | Earnings / Dividend Ex-Date / Macro-Related / Market Closure / Stock Split / IPO New Listing / Shareholder Meeting / Index Rebalancing, etc. |
| Multiple Events per Security | When a single security has multiple events, list all of them with aligned indentation |

---

## Section 2: Key Event Impact Analysis (Template 2)

In-depth expansion of high-importance events, helping users understand "what does this have to do with me?"

```text
🔍 Key Event Analysis

━━ [Event Name] · [HH:MM CST] ([Original Timezone]) ━━

[One sentence describing the event content and outcome]
Core Data: [Actual EPS vs Expected / Macro data actual vs expected / Policy key points]

Portfolio Impact:

● [Company Name] [Code] · [Market] · [Holdings/Watchlist] · Direct Impact
  Linkage Logic: [One sentence explaining why it's affected]
  Likely Direction: [Bullish / Bearish / Neutral]

● [Company Name] [Code] · [Market] · [Holdings/Watchlist] · Indirect Impact
  Linkage Logic: [One sentence]
  Likely Direction: [Bullish / Bearish / Neutral]

[Only list securities with direct or indirect impact; unrelated securities do not appear]

Action Reference: [One sentence, no buy/sell instructions]

━━ [Next Key Event] ━━
[Same format, continue analysis]
```

Field Rules:

| Field | Rule |
| ---- | ---- |
| Trigger Condition | Generated when high-importance events exist in the time range (major earnings, central bank decisions, non-farm payrolls, significant industry policies, etc.); omit entire Section 2 if none |
| Core Data | Preserve raw numbers (differentiated by client type per general rules) |
| Impact Level | Direct Impact / Indirect Impact — choose one. Only list securities with actual impact; unrelated securities do not appear in output |
| Multiple Events | Each key event gets its own block, listed sequentially with no cap |
| Action Reference | e.g., "Consider waiting 15 minutes after the open before making a judgment." No buy/sell instructions |

---

## Section 3: Earnings Results Express (Template 3)

Dedicated analysis of released earnings to help users quickly digest results.

```text
📢 Earnings Results Express

━━ [Company Name] [Code] · [Market] Earnings Released ━━

EPS: [Actual] vs Expected [Expected] ([+/-X%])
Key Highlight: [One sentence — the most critical business line metric]
Market Reaction: After-hours/Pre-market [+/-X%]

Portfolio Impact:

● [Company Name] [Code] · [Market] · [Holdings/Watchlist]
  [One-sentence conclusion: impact direction + suggested timing]

● [Company Name] [Code] · [Market] · [Holdings/Watchlist]
  [Same as above]

[Continue covering all related holdings and watchlist securities]

⚠️ [If next-day closure or half-day trading applies]
[Market Name] [Month Day] [Closed / Half-day trading until HH:MM CST] — watch for liquidity.

━━ [Next Company Earnings Results] ━━
[Same format]
```

Field Rules:

| Field | Rule |
| ---- | ---- |
| Trigger Condition | Limited to earnings released last night/pre-market today (between the previous trading day's close and today's open). Earlier historical earnings are not included. Omit entire Section 3 if none |
| EPS Line | Preserve raw numbers (differentiated by client type per general rules) |
| Beat/Miss Magnitude | Preserve percentage (differentiated by client type per general rules) |
| Market Reaction | After-hours/pre-market price change, reflecting market sentiment intensity |
| Timing Suggestion | Common references: "Consider waiting 15 minutes after the open before deciding", "May continue holding and observing" |
| Closure Notice | Only displayed when a market of interest has closure the next day; otherwise omitted |
| Multiple Earnings | Each company gets its own block, listed sequentially |

---

## Section 4: Market Trends & Opportunity Discovery (Template 4)

Goes beyond the user's holdings and watchlist to help discover market-level trends and potential opportunities.

```text
🔥 Market Trends & Opportunities

━━ Sector Trends ━━

[Trending Theme Name] (e.g., AI Computing, Nuclear Energy Revival, GLP-1 Weight-Loss Drugs, etc.)
  Background: [One sentence explaining why this theme is getting market attention]
  Representative Securities: [List of related stocks, with market indicated]
  Your Connection: [If overlap with user's holdings/watchlist, point it out; if none, state "You currently do not hold related securities"]

[More trending themes...]

━━ Cross-Market Linkage Signals ━━

[Signal Name] (e.g., A/H Premium Narrowing, Copper Price Transmission, Chinese ADR Spread, etc.)
  Yesterday's Situation: [Specific description of what happened, backed by data]
  Opportunity Logic: [Why this might be an opportunity]
  Related Securities: [Relevant stocks/ETFs, with market indicated]
  Risk Note: [One-sentence risk description]

[More linkage signals...]

━━ Event-Driven Opportunities ━━

[Event Name] → [Potential Opportunity]
  Logic: [How the event might create a trading window]
  Time Window: [Start and end of the opportunity window]
  Related Securities: [Relevant stocks, with market indicated]
  Risk Note: [One sentence]

[More event-driven opportunities...]
```

Field Rules:

| Field | Rule |
| ---- | ---- |
| Trigger Condition | Generated when WebSearch finds valuable market trends or opportunities; omit entire Section 4 if search yields no substantive findings |
| Sector Trends | The 2-3 most-watched themes/sectors in the current market; must have clear evidence of market attention (e.g., capital inflows, media coverage density, social discussion activity) |
| Cross-Market Linkage | Focus on yesterday's and recent cross-market signals, including A/H premiums, ADR spreads, commodity-stock correlations, exchange rate impacts, policy time-zone arbitrage, etc. |
| Event-Driven | Short-term opportunity windows potentially created by upcoming events (not limited to events related to user holdings) |
| User Connection | Each opportunity point should attempt to establish a link to user's holdings/watchlist; if none exists, explicitly state so |
| Risk Note | Every opportunity must include a risk description to maintain objectivity |
| No Buy/Sell Instructions | Only describe opportunity logic and risks; no "you should buy/sell" recommendations |

---

## General Rules

- **Generate as much as possible**: Do not artificially cap the number of events or securities — output as much relevant content as there is
- The four sections are concatenated in order, separated by dividers or blank lines
- Section 1 is the base section and must always be included; Sections 2, 3, and 4 are generated based on data availability
- All times are converted to Beijing Time (CST), with original timezone noted in parentheses
- Unrelated securities are simply omitted and do not appear in output
- Disclaimer text appears once at the very end of the complete report (once only) and must not be omitted
- Section 1: Full coverage of holdings/watchlist securities, plus market-wide high-attention event securities tagged as "Market" (marquee earnings, hot IPOs, industry leaders, etc.)
- Sections 2 & 3: Primarily focused on holdings and watchlist securities; major global events and trending securities directly related to the user's holdings/watchlist industries are permitted
- Section 4: Specifically designed for discovering opportunities beyond the portfolio; any security with investment value may appear
- Client type differentiated output rules:
  - **Fundamental client**: Preserve all raw numbers (EPS, beat percentage, macro data values, etc.)
  - **General retail client (commonsense)**: Convert professional metrics to everyday language (e.g., EPS → "earnings came in better/worse than expected"), omit specific numbers and percentages, replace with directional descriptions
