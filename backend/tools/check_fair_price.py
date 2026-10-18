from __future__ import annotations


def check_fair_price(price_tnd: float, expected_low: float, expected_high: float):
    """Simple market check that returns whether a proposed price is cheap, fair, or expensive."""

    if price_tnd < expected_low:
        return {"status": "cheap", "low": expected_low, "high": expected_high}
    if price_tnd > expected_high:
        return {"status": "expensive", "low": expected_low, "high": expected_high}
    return {"status": "fair", "low": expected_low, "high": expected_high}
