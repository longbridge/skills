# Wave Structure Reference

## Impulse Wave (推动浪)

5-wave structure in the direction of the trend:

```
          [5]
         /   \
        /     \
  [3] /        \
 /  \/          \
/   [4]          \
[1]
  \
  [2]
```

### Three Iron Rules (cannot be violated)
1. **Wave 2 must not retrace beyond the start of Wave 1**
   - If it does, the count is invalid — relabel from a higher degree
2. **Wave 3 cannot be the shortest impulse wave**
   - Wave 3 must be longer than at least one of Wave 1 or Wave 5
3. **Wave 4 must not enter the price territory of Wave 1**
   - Wave 4 low must remain above Wave 1 high (in a bullish impulse)
   - Exception: diagonal triangles (rare, not modelled in this engine)

### Wave Characteristics
| Wave | Typical Character |
|------|-------------------|
| Wave 1 | Trend initiation; often looks like a counter-trend bounce; volume moderate |
| Wave 2 | Deep retracement; feels like the prior trend resuming; volume declining |
| Wave 3 | **Strongest, longest** wave; highest volume; largest price move; fundamental news often appears |
| Wave 4 | Shallow correction; often sideways/choppy; lower volume than Wave 3 |
| Wave 5 | Final push; often narrowing breadth; divergence appears on momentum indicators |

## Corrective Wave (调整浪)

### Zigzag (5-3-5) — Most Common
```
[A]
   \
    \
    [B]
      \
       [C]
```
- A-wave: Initial decline (5-sub-waves internally)
- B-wave: Counter-trend bounce, retraces 38.2–61.8% of A
- C-wave: Final decline, typically equal to A in length

### Flat (3-3-5)
- B-wave retraces A deeply (78.6–100%)
- C-wave often equals A or extends to 1.618×A
- Common after strong Wave 3

### Triangle (3-3-3-3-3)
- Five sub-waves (A-B-C-D-E) in a converging pattern
- Typically appears as Wave 4 or Wave B
- Followed by a "thrust" in the direction of the prior trend

## Stage Labels and Market Position

| Stage | Description | What to Watch |
|-------|-------------|---------------|
| `impulse_early` (上升初段) | Wave 1 or early Wave 2 just completed — new uptrend starting | Breakout confirmation, volume pickup |
| `impulse_wave3` (主升段③浪) | In the middle of Wave 3 — strongest advance phase | Stay with the trend; no reversal signal is generated |
| `impulse_late` (上升末段⑤浪) | Wave 5 in progress — final leg, watch for divergence | Tighten stops; look for MACD/RSI bearish divergence |
| `top_zone` (顶部区域) | 5-wave advance just completed — reversal alert | Reduce longs; watch for ABC correction to begin |
| `corrective_abc` (调整段ABC) | In a corrective A-B-C structure after a 5-wave advance | Wait for C-wave completion; look for bullish divergence at C |
| `bottom_zone` (底部区域) | 5-wave decline completed or ABC correction ended | Potential reversal; confirm with momentum divergence |
| `unconfirmed` (结构待确认) | Two count interpretations conflict | Observe and wait; do not force a trade |

## Invalidation Rules

Each stage has a price level that, if breached, invalidates the count:

| Stage | Invalidation Level |
|-------|--------------------|
| `impulse_early` (Wave 2 in progress) | Below Wave 1 origin |
| `impulse_wave3` | Below Wave 1 high |
| `impulse_late` (Wave 5) | Below Wave 4 low |
| `top_zone` | Above Wave 5 high (would mean Wave 5 is extending) |
| `corrective_abc` | Below Wave A low × 1.618 (extreme C extension) |
| `bottom_zone` | Below the most recent Wave 5 low |

Always state the invalidation level explicitly in the output so the user knows the "stop" for the analysis.
