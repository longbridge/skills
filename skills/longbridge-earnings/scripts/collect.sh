#!/bin/sh
# collect.sh — parallel earnings-data collector for the longbridge-earnings skill.
#
# Usage:
#   collect.sh <SYMBOL> [--full]
#
# Fetches all CLI data sources needed for an earnings summary card in ONE
# parallel round (instead of ~10 sequential calls), trims the JSON with jq,
# and prints a compact digest to stdout. Raw responses are kept in the
# output directory for the full-report path to reuse.
#
#   lite  (default): snapshot, income statement (8Q), consensus, forecast-eps,
#                    quote, calc-index, institution-rating, segments, news, kline
#   --full extras  : balance sheet, cash flow, filing list, industry valuation,
#                    peer compare, rating history
#
# Requires: longbridge CLI (logged in), jq.

set -u

SYMBOL="${1:-}"
MODE="${2:-}"

if [ -z "$SYMBOL" ]; then
    echo "usage: collect.sh <SYMBOL> [--full]" >&2
    exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "ERROR: jq is required. Install jq, or run the longbridge commands manually." >&2
    exit 3
fi

if ! command -v longbridge >/dev/null 2>&1; then
    echo "ERROR: longbridge CLI not found. See SKILL.md 'MCP fallback'." >&2
    exit 3
fi

# HK symbols: leading zeros can cause empty results (09988.HK -> 9988.HK).
case "$SYMBOL" in
    0*.HK) SYMBOL=$(echo "$SYMBOL" | sed 's/^0*//');;
esac

OUT_DIR="/tmp/lb_earnings_$(echo "$SYMBOL" | tr 'A-Z.' 'a-z_')"
mkdir -p "$OUT_DIR"

# fetch <name> <args...> — run one CLI call, save raw JSON to $OUT_DIR/<name>.json.
# On failure the error text is saved to <name>.err instead; never blocks the rest.
fetch() {
    name="$1"; shift
    if longbridge "$@" --format json >"$OUT_DIR/$name.json" 2>"$OUT_DIR/$name.err"; then
        rm -f "$OUT_DIR/$name.err"
    else
        rm -f "$OUT_DIR/$name.json"
    fi
}

# ── Parallel fetch round ─────────────────────────────────────────────
fetch snapshot     financial-report snapshot "$SYMBOL" &
fetch is_qf        financial-report "$SYMBOL" --kind IS --report qf &
fetch consensus    consensus "$SYMBOL" &
fetch forecast_eps forecast-eps "$SYMBOL" &
fetch quote        quote "$SYMBOL" &
fetch calc_index   calc-index "$SYMBOL" &
fetch rating       institution-rating "$SYMBOL" &
fetch segments     business-segments "$SYMBOL" &
fetch news         news "$SYMBOL" --count 10 &
fetch kline        kline "$SYMBOL" --period day --count 250 &

if [ "$MODE" = "--full" ]; then
    fetch bs_qf      financial-report "$SYMBOL" --kind BS --report qf &
    fetch cf_qf      financial-report "$SYMBOL" --kind CF --report qf &
    fetch filings    filing "$SYMBOL" --count 10 &
    fetch ind_val    industry-valuation dist "$SYMBOL" &
    fetch compare    compare "$SYMBOL" &
    fetch rating_his institution-rating "$SYMBOL" --history &
fi
wait

# Quarterly income statement may be empty for semi-annual reporters: retry saf.
if [ ! -s "$OUT_DIR/is_qf.json" ] || [ "$(jq '[.list.IS.indicators[]?] | length' "$OUT_DIR/is_qf.json" 2>/dev/null)" = "0" ]; then
    fetch is_qf financial-report "$SYMBOL" --kind IS --report saf
fi

# ── Digest helpers ───────────────────────────────────────────────────
# slim: cut numeric-string precision (big numbers -> integers, ratios -> 2dp).
SLIM='def slim: walk(
    if type=="string" and test("^-?[0-9]+\\.[0-9]+$") then
        (tonumber as $n |
         if ($n | fabs) > 1000000 then ($n | round | tostring)
         else ((($n * 100) | round) / 100 | tostring) end)
    else . end);'

# section <title> <file> <jq-filter> — print trimmed JSON, or the saved error.
section() {
    title="$1"; file="$2"; filter="$3"
    echo "===== $title ====="
    if [ -s "$OUT_DIR/$file.json" ]; then
        jq -c "$SLIM $filter | slim" "$OUT_DIR/$file.json" 2>/dev/null \
            || echo "N/A (jq filter failed; raw: $OUT_DIR/$file.json)"
    elif [ -s "$OUT_DIR/$file.err" ]; then
        echo "N/A ($(head -c 200 "$OUT_DIR/$file.err" | tr '\n' ' '))"
    else
        echo "N/A (no data)"
    fi
}

# ── Digest to stdout ─────────────────────────────────────────────────
echo "SYMBOL: $SYMBOL"
echo "COLLECTED_AT: $(date '+%Y-%m-%d %H:%M %Z')"
echo "RAW_DIR: $OUT_DIR  (full statements/filings live here — reuse, do not re-fetch)"

# Latest-period summary incl. AI one-liner; drop empty est_* noise.
section "SNAPSHOT (latest period)" snapshot '
    walk(if type=="object" then with_entries(select(.value != "" and .value != null)) else . end)'

# Income statement: per indicator keep name + last 8 quarters, drop icon/router junk.
section "INCOME_STATEMENT (last 8 quarters)" is_qf '
    [.list[]?.indicators[]? | {
        title,
        accounts: [.accounts[]? | {
            name, field,
            values: [.values[0:8][]? | {period, value, yoy}]
        }]
    }]'

section "CONSENSUS (estimate vs actual, recent periods)" consensus '
    {currency, current_period,
     periods: [.list[0:6][]? | {
        fiscal_year, fiscal_period, period_text,
        details: [.details[]? | {key, name, estimate, actual, comp}]
     }]}'

section "FORECAST_EPS (annual consensus range, latest 3 windows)" forecast_eps '
    [.items[-3:][]? | {mean: .forecast_eps_mean, median: .forecast_eps_median,
                       high: .forecast_eps_highest, low: .forecast_eps_lowest}]'

section "QUOTE" quote '.'

section "CALC_INDEX (PE/PB/mktcap)" calc_index '.'

section "INSTITUTION_RATING" rating '.'

section "SEGMENTS (revenue breakdown)" segments '.'

section "NEWS (latest 10 headlines)" news '
    [.. | objects | select(has("title")) | {id, title, published_at}] | .[0:10]'

# K-line: last 20 sessions compact + 250-day high/low for context.
section "KLINE (20 recent closes + 250d range)" kline '
    ([.. | objects | select(has("close"))]) as $c |
    {recent: [$c[-20:][] | {d: ((.timestamp // .time // .date) | tostring | .[0:10]), c: .close}],
     high_250d: ([$c[].high | tonumber? // .] | max),
     low_250d:  ([$c[].low  | tonumber? // .] | min)}'

if [ "$MODE" = "--full" ]; then
    section "FILINGS (latest 10)" filings '
        [.. | objects | select(has("title") or has("name")) | {id, title: (.title // .name), date: (.published_at // .date // .filed_at)}] | .[0:10]'
    section "INDUSTRY_VALUATION (percentile dist)" ind_val '.'
    section "PEER_COMPARE" compare '
        [.list[]? | {name, counter_id, price_close, market_value, pe, pb, ps,
                     roe, roa, net_margin, div_yld, eps, sales, net_income}]'
    echo "===== FULL-MODE RAW FILES ====="
    echo "BS/CF statements, rating history: $OUT_DIR/{bs_qf,cf_qf,rating_his}.json"
fi
