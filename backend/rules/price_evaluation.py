from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PriceAssessment:
    label: str
    lower_bound_tnd: float
    upper_bound_tnd: float
    rationale: str


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
