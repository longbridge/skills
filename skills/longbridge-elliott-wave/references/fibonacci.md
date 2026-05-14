# Fibonacci Wave Relationships

## Impulse Wave (5-wave) Ratios

### Wave 2 vs Wave 1
| Retracement | Interpretation |
|-------------|----------------|
| 0.382 | Shallow correction — strong trend |
| 0.500 | Common |
| **0.618** | **Most common** |
| 0.786 | Deep correction — wave 2 still valid but weakening |
| > 0.786 | Suspect — may not be a valid wave 2 |

### Wave 3 vs Wave 1
| Ratio | Interpretation |
|-------|----------------|
| 1.000 | Minimum (equal) — weakest wave 3 |
| **1.618** | **Most common — "golden wave"** |
| 2.000 | Strong trend |
| 2.618 | Exhaustion extension |

Wave 3 is the most powerful impulse wave. It should have the highest volume.

### Wave 4 vs Wave 3
| Retracement | Interpretation |
|-------------|----------------|
| **0.382** | **Most common** |
| 0.236 | Very shallow — extremely strong trend |
| 0.500 | Maximum; must not enter wave 1 price territory |

### Wave 5 vs Wave 1
| Ratio | Interpretation |
|-------|----------------|
| **1.000** | **Most common (equality)** |
| 0.618 | Truncated wave 5 (bearish) |
| 1.618 | Extended wave 5 |

**Wave 5 failure** (price does not exceed wave 3 high): strong bearish signal — sharp reversal likely.

## Corrective Wave (ABC) Ratios

### Wave B vs Wave A
| Retracement | Correction Type |
|-------------|-----------------|
| 0.382–0.618 | Zigzag (most common) |
| 0.786–1.000 | Flat correction |
| > 1.000 | Irregular flat / expanded flat |

### Wave C vs Wave A
| Ratio | Interpretation |
|-------|----------------|
| **1.000** | **Equal — most common** |
| 0.618 | Short C-wave |
| 1.618 | Extended C-wave |

## Engine Tolerances

The signal engine uses ±15% tolerance on all targets:

| Relationship | Target Range | With ±15% Tolerance |
|---|---|---|
| Wave 2 / Wave 1 | 0.500–0.618 | 0.350–0.771 |
| Wave 3 / Wave 1 | 1.000–2.618 | 0.850–3.011 |
| Wave 4 / Wave 3 | 0.236–0.500 | 0.086–0.650 |
| ABC B / A | 0.382–0.618 | 0.232–0.771 |
| ABC C / A | 0.618–1.618 | 0.468–1.861 |

To tighten (fewer false signals): pass `--fib-tol 0.10`
To loosen (more signals): pass `--fib-tol 0.20`

## Key Price Zone Outputs

The engine outputs these Fibonacci price zones from the most recent swing high/low pair:

| Key | Formula | Use |
|-----|---------|-----|
| `retrace_0382` | High − 0.382 × span | Wave 4 support / first buy zone after wave 3 |
| `retrace_0500` | High − 0.500 × span | Mid support |
| `retrace_0618` | High − 0.618 × span | Deep support / wave 2 target |
| `retrace_0786` | High − 0.786 × span | Maximum corrective support |
| `extend_1000` | Low + 1.000 × span | Wave 5 / wave C equal target |
| `extend_1618` | Low + 1.618 × span | Wave 3 / extended wave C target |
| `extend_2618` | Low + 2.618 × span | Extended wave 3 target |
