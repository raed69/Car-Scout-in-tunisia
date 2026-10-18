from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CarAd:
    """What could be read from one search result. A field is None when the ad does not say it."""

    title: str
    url: str | None = None
    brand: str | None = None
    model: str | None = None
    price_tnd: int | None = None
    city: str | None = None
    year: int | None = None
    fuel: str | None = None
    transmission: str | None = None
    mileage_km: int | None = None
    source: str | None = None
