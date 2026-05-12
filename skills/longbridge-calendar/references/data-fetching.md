# Data Fetching Specification

## Overview

This file defines the data fetching strategy for the Skill at runtime, including what data is needed, where to get it, and what to do when it's unavailable.

## Longbridge CLI

Data is fetched via the `longbridge` command-line tool. The CLI is under continuous development — **do not assume any specific parameters**.

Before executing any command, you must first verify the currently supported subcommands and parameters via `--help`:

```bash
longbridge --help                          # Top-level command list
longbridge <command> --help                # Subcommands and options
longbridge <command> <subcommand> --help   # One level deeper
```

Check `--help` first, then execute the command. Do not skip this step. Follow the instructions from `--help` strictly — do not take extra actions, and when errors occur, re-check the supported command formats.

**Do not fabricate parameters.** Only use parameters explicitly listed in the `--help` output. If `--help` does not list a parameter (such as `--market`, `--start`, `--end`, `--symbol`, etc.), do not use it, even if you think it "should" exist.

**Fetch first, filter later.** Fetch data in the simplest way possible (usually with no or minimal parameters), then filter results based on user requirements (time, market, importance, etc.) after receiving the data. All filtering logic is performed after data retrieval.

## Required Data

### User Data (Non-Degradable)

| Data | Purpose | CLI Command Direction |
| --- | --- | --- |
| Holdings list | Determine the securities and markets the user cares about | `longbridge positions` |
| Watchlist | Same as above | `longbridge watchlist` |

Both must be obtained — neither may be omitted. Holdings and watchlist together constitute the user's complete scope of interest. If either fails to retrieve, terminate the personalized flow and prompt the user to check their login status (`longbridge auth login`).

### Financial Calendar Data (Degradable to WebSearch)

| Data | CLI Command Direction |
| --- | --- |
| Earnings/Performance Calendar | Related subcommands under `longbridge finance-calendar` |
| Macroeconomic Calendar | Same as above |
| Dividend/Ex-Date Calendar | Same as above |
| Market Closure/Trading Calendar | Same as above |
| Stock Split Calendar | Same as above |
| IPO/New Listing | Same as above |

`finance-calendar` has multiple subcommands (such as report, macrodata, dividend, closed, split, ipo, etc.). Verify the exact usage and supported filter parameters via `longbridge finance-calendar --help` and each subcommand's `--help`.

Key tip: The earnings calendar return data typically already includes expected and actual EPS values — no additional commands are needed to fetch them.

**Important: Fetch market-wide data; do not filter by holdings/watchlist.**

Calendar data should be fetched uniformly **without the `--filter` parameter**, pulling all market-wide events in one request. After retrieving the data, tag each event based on the holdings and watchlist:

1. Security is in the holdings list → tag as "Holdings"
2. Security is in the watchlist → tag as "Watchlist"
3. Neither → evaluate importance to decide whether to include; if worthy, tag as "Market"

This way, data only needs to be fetched once. Tags are purely post-processing classification and do not affect data retrieval scope. **Do not use `--filter watchlist` or `--filter positions`** — this would cause market-wide events to be lost, eliminating the opportunity discovery capability.

### Stock Code Format

Longbridge uses the `<CODE>.<MARKET>` format (e.g., `AAPL.US`, `700.HK`, `600519.SH`). See the top of `longbridge --help` for supported market suffixes.

### Market Trends & Opportunity Data (Proactively Fetched via WebSearch)

This data does not depend on the CLI. It is **proactively searched** via WebSearch and executed **in parallel** with CLI data collection.

| Data | Search Strategy | Example Search Keywords |
| --- | --- | --- |
| Sector trends & capital flows | Search for current/recent market hot sectors, capital flows, thematic investment trends | `A-share sector gains capital inflow today`, `US stock market sector rotation today`, `HK stock sector trends` |
| Cross-market linkage signals | Search for A/H premiums, ADR spreads, commodity-stock correlations, etc. | `AH share premium index today`, `Chinese ADR premium`, `copper price mining stock correlation`, `cross market arbitrage signals` |
| Market sentiment & trending topics | Search investment community hot topics, stocks with unusual activity | `market trending topics today`, `stock market trending today`, `HK stock unusual activity` |
| Event-driven opportunities | Based on already-fetched calendar events, search for related trading strategies and opportunity analysis | `[event name] trading strategy`, `earnings trade opportunity [ticker]` |

**Search Principles:**
- Searches should cover all markets represented in the user's holdings (US, HK, A-shares, etc.), not limited to a single market
- Prioritize authoritative financial media and professional analysis (e.g., Bloomberg, Reuters, Caixin, East Money, ET Net, etc.)
- Search terms should include today's date or "today" to ensure timeliness
- Cross-market linkage analysis should focus on signals that "already occurred yesterday but may transmit to other markets"
- Execute at least 1-2 searches per search direction; decide whether to go deeper based on result quality

## Degradation Rules

1. **User data is non-degradable**: Holdings and watchlist must be obtained via CLI. When unauthorized, only provide the global financial calendar query.
2. **Calendar data is degradable**: When CLI calls fail or return empty results, supplement with WebSearch, prioritizing authoritative financial websites (exchange announcements, company IR pages, mainstream financial media).
3. **Market trends data has no degradation concept**: It is inherently obtained via WebSearch. If searches yield no valuable results, Section 4 is simply omitted.
4. When degrading, there is no need to inform the user about data source differences.
