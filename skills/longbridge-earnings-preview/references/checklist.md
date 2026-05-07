# Earnings Preview Checklist

## Pre-Report Data Collection

- [ ] Confirmed earnings date and time (pre-market vs. after-hours)
- [ ] Consensus estimates sourced with date (revenue, EPS, key metrics)
- [ ] Prior quarter results and management guidance reviewed
- [ ] Recent filings checked via `longbridge filing SYMBOL --count 5 --format json 2>/dev/null`
- [ ] Recent news scanned via `longbridge news SYMBOL --count 10 --format json 2>/dev/null`
- [ ] Current price and valuation via `longbridge quote` and `longbridge calc-index`
- [ ] Historical earnings reaction pattern researched (web search)
- [ ] Options-implied move checked (web search)

## Analysis Quality

- [ ] Bull/base/bear scenarios have specific, quantified assumptions
- [ ] Key metrics ranked by importance (what will move the stock most?)
- [ ] Catalyst checklist identifies 3-5 binary decision points
- [ ] Historical context provided (how has stock reacted to similar prints?)
- [ ] Consensus source and date clearly noted

## Output Format

- [ ] One-page format (no longer than necessary)
- [ ] Consensus estimates table included
- [ ] Scenario table with stock reaction estimates
- [ ] Catalyst checklist with ranked priorities
- [ ] Trading setup section with price trend and positioning data
