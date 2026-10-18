from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CarAd:
    """A normalized representation of a single car listing."""

    title: str
    brand: str
    model: str
    price_tnd: float
    city: str
    year: int | None = None
    fuel: str | None = None
    transmission: str | None = None
    mileage_km: int | None = None
    url: str | None = None
    source: str | None = None
