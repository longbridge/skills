#!/usr/bin/env python3
"""Fetch FXMacroData release-calendar rows as JSON."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional


DEFAULT_BASE_URL = "https://fxmacrodata.com/api/v1"


def fetch_calendar(
    currency: str,
    limit: int,
    min_tier: Optional[int],
    api_key: Optional[str],
    base_url: str,
) -> list[dict]:
    limit_count = max(1, min(int(limit), 100))
    params: dict[str, str] = {"limit": str(limit_count)}
    if min_tier is not None:
        params["min_tier"] = str(min_tier)
    if api_key:
        params["api_key"] = api_key

    url = (
        f"{base_url.rstrip('/')}/calendar/{urllib.parse.quote(currency.lower())}"
        f"?{urllib.parse.urlencode(params)}"
    )
    request = urllib.request.Request(url, headers={"Accept": "application/json"})

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"FXMacroData request failed with HTTP {exc.code}: {detail}") from exc

    rows = payload.get("data", payload)
    if not isinstance(rows, list):
        raise RuntimeError("FXMacroData response did not contain a calendar row list")
    if min_tier is not None:
        rows = [
            row
            for row in rows
            if int(row.get("market_tier") or 99) <= min_tier
        ]
    return rows[:limit_count]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--currency", default="usd", help="Three-letter currency code.")
    parser.add_argument("--limit", type=int, default=25, help="Maximum number of rows.")
    parser.add_argument("--min-tier", type=int, default=1, help="Minimum event tier.")
    parser.add_argument("--api-key", default=os.getenv("FXMACRODATA_API_KEY"))
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = parser.parse_args()

    rows = fetch_calendar(
        currency=args.currency,
        limit=args.limit,
        min_tier=args.min_tier,
        api_key=args.api_key,
        base_url=args.base_url,
    )
    json.dump(rows, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
