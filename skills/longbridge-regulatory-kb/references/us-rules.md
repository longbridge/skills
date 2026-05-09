# US Stock Rules — Full Reference

## Pattern Day Trader (PDT) Rule

- Applies to margin accounts at US broker-dealers.
- **Definition**: 4+ day trades in a rolling 5-business-day period AND day trades > 6% of total trades.
- **Requirement**: Minimum $25,000 equity in the account.
- **Consequence if below $25k**: Account restricted to closing trades for 90 days.
- **Workaround**: Cash account (no PDT), trade futures/options, or use non-US brokers.

## Margin (Reg T / FINRA)

- **Reg T**: Initial margin = 50% of purchase price for equity securities.
- **FINRA Rule 4210**: Maintenance margin = 25% of market value (brokers often require 30%).
- **Pattern day trader maintenance**: 25% minimum for day trades.
- **Margin call**: Must meet within 3 business days; broker may liquidate positions.

## Settlement

- **T+1** for US equities effective May 28, 2024 (previously T+2).
- Options: T+1 standard.
- US Treasuries: T+1.

## Circuit Breakers (熔断)

| Trigger | Market decline | Action |
|---|---|---|
| Level 1 | S&P 500 down 7% | 15-minute halt (before 3:25 PM ET) |
| Level 2 | S&P 500 down 13% | 15-minute halt (before 3:25 PM ET) |
| Level 3 | S&P 500 down 20% | Market closes for the rest of the day |

Individual stock circuit breakers: LULD (Limit Up-Limit Down) bands, typically ±5% for most stocks in a 5-minute window.

## Short Selling (做空)

- **Reg SHO**: Must locate shares before short selling; failure to deliver triggers buy-in.
- **Uptick rule (Rule 10a-1 alternative)**: If stock drops >10% in one day, short selling only permitted on an uptick for the remainder of that day and the next.

## SEC Reporting

| Filing | Who | Deadline |
|---|---|---|
| 13F | Institutions > $100M AUM | 45 days after quarter end |
| Form 4 | Directors / officers | 2 business days after transaction |
| 8-K | Public companies | 4 business days after material event |
| 10-K | Public companies | 60-90 days after fiscal year end |
| 10-Q | Public companies | 40-45 days after quarter end |
