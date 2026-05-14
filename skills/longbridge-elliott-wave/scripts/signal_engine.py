"""Elliott Wave signal engine for Longbridge kline data.

Workflow:
1. Parse Longbridge kline JSON (daily candles)
2. ZigZag swing-point detection (rolling window, price-threshold filter)
3. 5-wave impulse matching + three iron rule validation
4. ABC corrective matching
5. Fibonacci ratio validation
6. Stage labeling + Fibonacci price zones
7. Output structured JSON for SKILL.md to render

Usage:
    python3 signal_engine.py --kline /tmp/kline_day.json --symbol AAPL.US
    python3 signal_engine.py --kline /tmp/kline_day.json --symbol 700.HK --threshold 0.03

Dependencies:
    pip install pandas numpy
"""

import argparse
import json
import sys
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Market-specific ZigZag thresholds (price move % to qualify as a swing)
# ---------------------------------------------------------------------------
MARKET_THRESHOLDS = {
    "HK": 0.03,
    "US": 0.03,
    "SH": 0.02,
    "SZ": 0.02,
    "SGX": 0.03,
}

STAGE_LABELS = {
    "impulse_early": "impulse_early",
    "impulse_wave3": "impulse_wave3",
    "impulse_late": "impulse_late",
    "top_zone": "top_zone",
    "corrective_abc": "corrective_abc",
    "bottom_zone": "bottom_zone",
    "unconfirmed": "unconfirmed",
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_longbridge_kline(path: str) -> pd.DataFrame:
    """Load Longbridge kline JSON into a DataFrame.

    Longbridge kline JSON schema (--format json):
        List of objects with keys: time, open, high, low, close, volume, turnover
        time is a datetime string, e.g. "2025-03-03 05:00:00".

    Returns:
        DataFrame with datetime index and columns: open, high, low, close, volume.

    Raises:
        ValueError: if required columns are missing or data is empty.
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if not raw:
        raise ValueError("Empty kline data")

    df = pd.DataFrame(raw)

    # Normalise column names (Longbridge uses lowercase)
    df.columns = [c.lower() for c in df.columns]

    # Support both "time" (string) and "timestamp" (epoch int) field names
    if "time" in df.columns and "timestamp" not in df.columns:
        df = df.rename(columns={"time": "timestamp"})

    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in kline JSON: {missing}")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp").sort_index()

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["high", "low", "close"])
    return df


# ---------------------------------------------------------------------------
# ZigZag swing detection
# ---------------------------------------------------------------------------

def find_swings(
    high: pd.Series,
    low: pd.Series,
    window: int = 10,
    threshold: float = 0.03,
) -> List[Dict]:
    """Detect alternating ZigZag swing highs and lows.

    Uses two passes:
    1. Rolling-window local extremes to find candidate swings.
    2. Price-threshold filter: only keep swings where price move from
       previous swing exceeds `threshold` (as a fraction of price).

    Args:
        high: Daily high price series.
        low: Daily low price series.
        window: Half-window for rolling extreme detection (full = 2*window+1).
        threshold: Minimum price move fraction to qualify as a swing.

    Returns:
        List of dicts: {"index": Timestamp, "price": float, "type": "H"|"L"}.
        Guaranteed alternating H/L sequence.
    """
    full_w = window * 2 + 1
    if len(high) < full_w:
        return []

    roll_max = high.rolling(full_w, center=True).max()
    roll_min = low.rolling(full_w, center=True).min()

    raw_points = []
    for idx in high.index:
        is_h = bool(high[idx] == roll_max[idx]) if not pd.isna(roll_max[idx]) else False
        is_l = bool(low[idx] == roll_min[idx]) if not pd.isna(roll_min[idx]) else False
        if is_h and not is_l:
            raw_points.append({"index": idx, "price": float(high[idx]), "type": "H"})
        elif is_l and not is_h:
            raw_points.append({"index": idx, "price": float(low[idx]), "type": "L"})

    if len(raw_points) < 2:
        return raw_points

    # Deduplicate to strictly alternating sequence, keep most extreme
    zigzag = [raw_points[0]]
    for pt in raw_points[1:]:
        if pt["type"] == zigzag[-1]["type"]:
            if pt["type"] == "H" and pt["price"] > zigzag[-1]["price"]:
                zigzag[-1] = pt
            elif pt["type"] == "L" and pt["price"] < zigzag[-1]["price"]:
                zigzag[-1] = pt
        else:
            zigzag.append(pt)

    # Apply price-threshold filter: remove swing if move < threshold
    filtered = [zigzag[0]]
    for pt in zigzag[1:]:
        prev_price = filtered[-1]["price"]
        move = abs(pt["price"] - prev_price) / prev_price
        if move >= threshold:
            if pt["type"] == filtered[-1]["type"]:
                if pt["type"] == "H" and pt["price"] > filtered[-1]["price"]:
                    filtered[-1] = pt
                elif pt["type"] == "L" and pt["price"] < filtered[-1]["price"]:
                    filtered[-1] = pt
            else:
                filtered.append(pt)

    return filtered


# ---------------------------------------------------------------------------
# Fibonacci validation
# ---------------------------------------------------------------------------

def check_fib_ratios(
    w1: float, w2: float, w3: float, w4: float, w5: float, tol: float = 0.15
) -> bool:
    """Validate Fibonacci wave relationships for a 5-wave impulse.

    Checks:
    - Wave 2 retraces wave 1 by 0.5–0.618
    - Wave 3 / wave 1 in range 1.0–2.618
    - Wave 4 retraces wave 3 by 0.236–0.5

    Args:
        w1..w5: Absolute amplitudes of each wave.
        tol: Tolerance added/subtracted from target ranges.

    Returns:
        True if all checks pass.
    """
    if w1 == 0 or w3 == 0:
        return False

    r2 = w2 / w1
    if not (0.5 - tol <= r2 <= 0.618 + tol):
        return False

    r3 = w3 / w1
    if not (1.0 - tol <= r3 <= 2.618 + tol):
        return False

    r4 = w4 / w3
    if not (0.236 - tol <= r4 <= 0.5 + tol):
        return False

    return True


def check_abc_fib(
    wave_a: float, wave_b: float, wave_c: float, tol: float = 0.15
) -> bool:
    """Validate Fibonacci ratios for an ABC corrective wave.

    Checks:
    - B retraces A by 0.382–0.618
    - C is 0.618–1.618 times A

    Args:
        wave_a, wave_b, wave_c: Absolute amplitudes.
        tol: Tolerance.

    Returns:
        True if checks pass.
    """
    if wave_a == 0:
        return False

    r_b = wave_b / wave_a
    if not (0.382 - tol <= r_b <= 0.618 + tol):
        return False

    r_c = wave_c / wave_a
    if not (0.618 - tol <= r_c <= 1.618 + tol):
        return False

    return True


def min_bars_ok(swings: List[Dict], start: int, count: int, min_bars: int = 5) -> bool:
    """Check that each wave spans at least min_bars calendar days."""
    for i in range(start, start + count - 1):
        diff = abs((swings[i + 1]["index"] - swings[i]["index"]).days)
        if diff < min_bars:
            return False
    return True


# ---------------------------------------------------------------------------
# Impulse (5-wave) detection
# ---------------------------------------------------------------------------

def find_impulse(swings: List[Dict], fib_tol: float = 0.15) -> List[Dict]:
    """Find completed 5-wave impulse structures.

    Bullish impulse: L-H-L-H-L-H (6 points, 5 segments)
    Bearish impulse: H-L-H-L-H-L (6 points, 5 segments)

    Returns:
        List of dicts with keys: end_time, direction (-1 sell / 1 buy),
        waves (list of 6 swing points), amplitudes (w1..w5).
    """
    results = []
    for i in range(len(swings) - 5):
        seg = swings[i: i + 6]
        types = [s["type"] for s in seg]

        if types == ["L", "H", "L", "H", "L", "H"]:
            x, p1, p2, p3, p4, p5 = seg
            w1 = p1["price"] - x["price"]
            w2 = p1["price"] - p2["price"]
            w3 = p3["price"] - p2["price"]
            w4 = p3["price"] - p4["price"]
            w5 = p5["price"] - p4["price"]

            if any(v <= 0 for v in [w1, w3, w5]):
                continue
            if p2["price"] <= x["price"]:     # Iron rule 1
                continue
            if w3 < w1 and w3 < w5:           # Iron rule 2
                continue
            if p4["price"] <= p1["price"]:    # Iron rule 3
                continue
            if not min_bars_ok(swings, i, 6):
                continue
            if not check_fib_ratios(w1, w2, w3, w4, w5, fib_tol):
                continue

            results.append({
                "end_time": p5["index"],
                "direction": -1,              # 5-wave up complete → sell signal
                "type": "bullish_impulse",
                "waves": seg,
                "amplitudes": {"w1": w1, "w2": w2, "w3": w3, "w4": w4, "w5": w5},
            })

        elif types == ["H", "L", "H", "L", "H", "L"]:
            x, p1, p2, p3, p4, p5 = seg
            w1 = x["price"] - p1["price"]
            w2 = p2["price"] - p1["price"]
            w3 = p2["price"] - p3["price"]
            w4 = p4["price"] - p3["price"]
            w5 = p4["price"] - p5["price"]

            if any(v <= 0 for v in [w1, w3, w5]):
                continue
            if p2["price"] >= x["price"]:
                continue
            if w3 < w1 and w3 < w5:
                continue
            if p4["price"] >= p1["price"]:
                continue
            if not min_bars_ok(swings, i, 6):
                continue
            if not check_fib_ratios(w1, w2, w3, w4, w5, fib_tol):
                continue

            results.append({
                "end_time": p5["index"],
                "direction": 1,               # 5-wave down complete → buy signal
                "type": "bearish_impulse",
                "waves": seg,
                "amplitudes": {"w1": w1, "w2": w2, "w3": w3, "w4": w4, "w5": w5},
            })

    return results


# ---------------------------------------------------------------------------
# ABC corrective detection
# ---------------------------------------------------------------------------

def find_abc(swings: List[Dict], fib_tol: float = 0.15) -> List[Dict]:
    """Find completed ABC corrective structures.

    Bearish ABC (after uptrend): H-L-H-L → correction complete → buy
    Bullish ABC (after downtrend): L-H-L-H → correction complete → sell

    Returns:
        List of dicts with keys: end_time, direction, type, waves, amplitudes.
    """
    results = []
    for i in range(len(swings) - 3):
        seg = swings[i: i + 4]
        types = [s["type"] for s in seg]

        if types == ["H", "L", "H", "L"]:
            start, pa, pb, pc = seg
            wa = start["price"] - pa["price"]
            wb = pb["price"] - pa["price"]
            wc = pb["price"] - pc["price"]

            if any(v <= 0 for v in [wa, wb, wc]):
                continue
            if pb["price"] >= start["price"]:
                continue
            if not check_abc_fib(wa, wb, wc, fib_tol):
                continue
            if not min_bars_ok(swings, i, 4):
                continue

            results.append({
                "end_time": pc["index"],
                "direction": 1,               # bearish ABC complete → buy
                "type": "bearish_abc",
                "waves": seg,
                "amplitudes": {"wa": wa, "wb": wb, "wc": wc},
            })

        elif types == ["L", "H", "L", "H"]:
            start, pa, pb, pc = seg
            wa = pa["price"] - start["price"]
            wb = pa["price"] - pb["price"]
            wc = pc["price"] - pb["price"]

            if any(v <= 0 for v in [wa, wb, wc]):
                continue
            if pb["price"] <= start["price"]:
                continue
            if not check_abc_fib(wa, wb, wc, fib_tol):
                continue
            if not min_bars_ok(swings, i, 4):
                continue

            results.append({
                "end_time": pc["index"],
                "direction": -1,              # bullish ABC complete → sell
                "type": "bullish_abc",
                "waves": seg,
                "amplitudes": {"wa": wa, "wb": wb, "wc": wc},
            })

    return results


# ---------------------------------------------------------------------------
# Stage labeling
# ---------------------------------------------------------------------------

def label_stage(
    swings: List[Dict],
    current_price: float,
    impulses: List[Dict],
    corrections: List[Dict],
) -> Tuple[str, Optional[Dict]]:
    """Derive the current wave stage label from recent pattern matches.

    Strategy: use the most recent completed pattern and the position of
    the current price relative to the last few swings to infer stage.

    Args:
        swings: Full swing sequence.
        current_price: Latest close price.
        impulses: List of detected impulse completions.
        corrections: List of detected ABC completions.

    Returns:
        (stage_label, context_dict) where context_dict has info for output.
    """
    # Collect all detected events sorted by time
    all_events = [
        {"time": e["end_time"], "event_type": e["type"], "direction": e["direction"], "data": e}
        for e in (impulses + corrections)
    ]
    all_events.sort(key=lambda x: x["time"])

    if not all_events:
        # No complete pattern — infer from swing position
        if len(swings) >= 4:
            last = swings[-1]
            prev = swings[-3] if len(swings) >= 3 else swings[0]
            if last["type"] == "H" and current_price > prev["price"] * 0.97:
                return "impulse_early", None
        return "unconfirmed", None

    latest = all_events[-1]

    # After bullish impulse completion (5-wave up done) → top zone
    if latest["event_type"] == "bullish_impulse":
        return "top_zone", latest["data"]

    # After bearish impulse completion (5-wave down done) → bottom zone
    if latest["event_type"] == "bearish_impulse":
        return "bottom_zone", latest["data"]

    # After bearish ABC completion (correction after uptrend done) → early impulse
    if latest["event_type"] == "bearish_abc":
        return "impulse_early", latest["data"]

    # After bullish ABC completion (correction after downtrend done) → corrective continuation
    if latest["event_type"] == "bullish_abc":
        return "corrective_abc", latest["data"]

    return "unconfirmed", None


# ---------------------------------------------------------------------------
# Fibonacci price zones
# ---------------------------------------------------------------------------

def compute_fib_zones(swings: List[Dict]) -> Dict[str, float]:
    """Compute Fibonacci retracement and extension zones from recent swings.

    Uses the most recent significant swing high and low pair.

    Returns:
        Dict mapping level name to price.
    """
    if len(swings) < 2:
        return {}

    # Find most recent swing high and low
    recent = swings[-8:] if len(swings) >= 8 else swings
    highs = [s for s in recent if s["type"] == "H"]
    lows = [s for s in recent if s["type"] == "L"]

    if not highs or not lows:
        return {}

    swing_high = max(highs, key=lambda s: s["price"])["price"]
    swing_low = min(lows, key=lambda s: s["price"])["price"]
    span = swing_high - swing_low

    if span == 0:
        return {}

    return {
        "high": round(swing_high, 4),
        "low": round(swing_low, 4),
        "retrace_0382": round(swing_high - 0.382 * span, 4),
        "retrace_0500": round(swing_high - 0.500 * span, 4),
        "retrace_0618": round(swing_high - 0.618 * span, 4),
        "retrace_0786": round(swing_high - 0.786 * span, 4),
        "extend_1000": round(swing_low + 1.000 * span, 4),
        "extend_1618": round(swing_low + 1.618 * span, 4),
        "extend_2618": round(swing_low + 2.618 * span, 4),
    }


# ---------------------------------------------------------------------------
# Module B: Momentum indicators
# ---------------------------------------------------------------------------

def compute_momentum(df: pd.DataFrame) -> Dict:
    """Compute MACD, RSI, MA, and volume signals from OHLCV data.

    Args:
        df: DataFrame with columns high, low, close, volume.

    Returns:
        Dict with indicator values and divergence flags.
    """
    close = df["close"]
    volume = df["volume"]
    n = len(close)

    result = {}

    # --- MACD (12/26/9 EMA) ---
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line

    result["macd"] = {
        "line": round(float(macd_line.iloc[-1]), 6),
        "signal": round(float(signal_line.iloc[-1]), 6),
        "histogram": round(float(histogram.iloc[-1]), 6),
        "above_signal": bool(macd_line.iloc[-1] > signal_line.iloc[-1]),
        "histogram_rising": bool(histogram.iloc[-1] > histogram.iloc[-2]) if n >= 2 else None,
    }

    # Bearish divergence: price makes higher high, MACD makes lower high (last 20 bars)
    window = min(20, n)
    price_window = close.iloc[-window:]
    macd_window = macd_line.iloc[-window:]
    bearish_div = bool(
        price_window.iloc[-1] > price_window.max() * 0.97
        and macd_window.iloc[-1] < macd_window.max() * 0.85
    )
    bullish_div = bool(
        price_window.iloc[-1] < price_window.min() * 1.03
        and macd_window.iloc[-1] > macd_window.min() * 0.85
    )
    result["macd"]["bearish_divergence"] = bearish_div
    result["macd"]["bullish_divergence"] = bullish_div

    # --- RSI (14) ---
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - 100 / (1 + rs)

    rsi_val = float(rsi.iloc[-1])
    result["rsi"] = {
        "value": round(rsi_val, 2),
        "overbought": rsi_val > 70,
        "oversold": rsi_val < 30,
    }

    # RSI divergence (same window)
    rsi_window = rsi.iloc[-window:]
    result["rsi"]["bearish_divergence"] = bool(
        price_window.iloc[-1] > price_window.max() * 0.97
        and rsi_window.iloc[-1] < rsi_window.max() * 0.85
    )
    result["rsi"]["bullish_divergence"] = bool(
        price_window.iloc[-1] < price_window.min() * 1.03
        and rsi_window.iloc[-1] > rsi_window.min() * 0.85
    )

    # --- Moving averages ---
    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()
    current_close = float(close.iloc[-1])

    result["ma"] = {
        "ma20": round(float(ma20.iloc[-1]), 4) if not pd.isna(ma20.iloc[-1]) else None,
        "ma50": round(float(ma50.iloc[-1]), 4) if not pd.isna(ma50.iloc[-1]) else None,
        "above_ma20": bool(current_close > ma20.iloc[-1]) if not pd.isna(ma20.iloc[-1]) else None,
        "above_ma50": bool(current_close > ma50.iloc[-1]) if not pd.isna(ma50.iloc[-1]) else None,
        "ma20_slope_up": bool(ma20.iloc[-1] > ma20.iloc[-5]) if n >= 5 and not pd.isna(ma20.iloc[-5]) else None,
    }

    # --- Volume ---
    vol_ma20 = volume.rolling(20).mean()
    result["volume"] = {
        "latest": int(volume.iloc[-1]),
        "ma20": int(vol_ma20.iloc[-1]) if not pd.isna(vol_ma20.iloc[-1]) else None,
        "above_average": bool(volume.iloc[-1] > vol_ma20.iloc[-1]) if not pd.isna(vol_ma20.iloc[-1]) else None,
        "expanding_vs_prev_3": bool(
            float(volume.iloc[-1]) > float(volume.iloc[-4:-1].mean())
        ) if n >= 4 else None,
    }

    return result


# ---------------------------------------------------------------------------
# Main analysis function
# ---------------------------------------------------------------------------

def analyse(
    kline_path: str,
    symbol: str,
    threshold: Optional[float] = None,
    fib_tol: float = 0.15,
    swing_window: int = 10,
) -> Dict:
    """Run full Elliott Wave analysis on a symbol.

    Args:
        kline_path: Path to Longbridge kline JSON file.
        symbol: Symbol string (e.g. "AAPL.US", "700.HK").
        threshold: ZigZag price-move threshold (auto-detected from market if None).
        fib_tol: Fibonacci ratio tolerance.
        swing_window: Rolling window half-size for swing detection.

    Returns:
        Analysis result dict ready for JSON serialisation.
    """
    df = load_longbridge_kline(kline_path)

    if len(df) < 250:
        return {
            "symbol": symbol,
            "error": "insufficient_data",
            "bars": len(df),
            "message": "Fewer than 250 daily candles — wave count unreliable.",
        }

    # Determine ZigZag threshold from market suffix
    if threshold is None:
        market = symbol.split(".")[-1].upper() if "." in symbol else "US"
        threshold = MARKET_THRESHOLDS.get(market, 0.03)

    current_price = float(df["close"].iloc[-1])
    swings = find_swings(df["high"], df["low"], window=swing_window, threshold=threshold)

    if len(swings) < 4:
        return {
            "symbol": symbol,
            "stage": "unconfirmed",
            "agreed": False,
            "message": "Not enough swing points for wave count.",
            "current_price": current_price,
            "fib_zones": compute_fib_zones(swings),
            "momentum": compute_momentum(df),
            "swings": _serialise_swings(swings[-10:]),
        }

    # Run wave detection
    impulses = find_impulse(swings, fib_tol)
    corrections = find_abc(swings, fib_tol)

    # Primary count
    stage_a, context_a = label_stage(swings, current_price, impulses, corrections)

    # Secondary count: re-run with slightly different threshold (+20%) for robustness
    swings_b = find_swings(df["high"], df["low"], window=swing_window, threshold=threshold * 1.2)
    impulses_b = find_impulse(swings_b, fib_tol)
    corrections_b = find_abc(swings_b, fib_tol)
    stage_b, _ = label_stage(swings_b, current_price, impulses_b, corrections_b)

    agreed = stage_a == stage_b
    final_stage = stage_a if agreed else "unconfirmed"

    fib_zones = compute_fib_zones(swings)
    momentum = compute_momentum(df)

    return {
        "symbol": symbol,
        "current_price": current_price,
        "stage": final_stage,
        "count_a": stage_a,
        "count_b": stage_b,
        "agreed": agreed,
        "fib_zones": fib_zones,
        "momentum": momentum,
        "recent_impulses": len(impulses),
        "recent_corrections": len(corrections),
        "swings": _serialise_swings(swings[-12:]),
        "bars_analysed": len(df),
        "threshold_used": threshold,
    }


def _serialise_swings(swings: List[Dict]) -> List[Dict]:
    """Convert swing dicts to JSON-serialisable form."""
    out = []
    for s in swings:
        out.append({
            "date": s["index"].strftime("%Y-%m-%d") if hasattr(s["index"], "strftime") else str(s["index"]),
            "price": s["price"],
            "type": s["type"],
        })
    return out


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Elliott Wave analysis engine for Longbridge kline data."
    )
    parser.add_argument("--kline", required=True, help="Path to Longbridge kline JSON file")
    parser.add_argument("--symbol", required=True, help="Symbol, e.g. AAPL.US or 700.HK")
    parser.add_argument(
        "--threshold", type=float, default=None,
        help="ZigZag price-move threshold (default: auto from market)"
    )
    parser.add_argument(
        "--fib-tol", type=float, default=0.15,
        help="Fibonacci ratio tolerance (default: 0.15)"
    )
    parser.add_argument(
        "--window", type=int, default=10,
        help="Swing detection half-window (default: 10)"
    )
    args = parser.parse_args()

    result = analyse(
        kline_path=args.kline,
        symbol=args.symbol,
        threshold=args.threshold,
        fib_tol=args.fib_tol,
        swing_window=args.window,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
