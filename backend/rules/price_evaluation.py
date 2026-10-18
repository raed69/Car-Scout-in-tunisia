from __future__ import annotations

from dataclasses import dataclass
from statistics import median

# With fewer prices than this, the "normal" price is too uncertain to call anything cheap or expensive.
MIN_PRICES_FOR_MARKET = 3
MARKET_SPREAD = 0.15


@dataclass
class PriceAssessment:
    label: str
    lower_bound_tnd: float
    upper_bound_tnd: float
    rationale: str


def market_range(prices: list[float]) -> tuple[float, float] | None:
    """Estimate the normal price band from the prices of similar ads: the middle price, plus or minus 15%."""

    if len(prices) < MIN_PRICES_FOR_MARKET:
        return None
    middle = median(prices)
    return middle * (1 - MARKET_SPREAD), middle * (1 + MARKET_SPREAD)


def assess_price(price_tnd: float, expected_range: tuple[float, float]) -> PriceAssessment:
    """Return a simple fair-price assessment based on a market range."""

    low, high = expected_range
    if price_tnd < low * 0.9:
        return PriceAssessment(
            label="cheap",
            lower_bound_tnd=low,
            upper_bound_tnd=high,
            rationale="This price sits below the expected market band, which may indicate a good opportunity.",
        )
    if price_tnd > high * 1.1:
        return PriceAssessment(
            label="expensive",
            lower_bound_tnd=low,
            upper_bound_tnd=high,
            rationale="This price is above the expected range and may not be competitive.",
        )
    return PriceAssessment(
        label="fair",
        lower_bound_tnd=low,
        upper_bound_tnd=high,
        rationale="This price looks broadly aligned with the current market range.",
    )
