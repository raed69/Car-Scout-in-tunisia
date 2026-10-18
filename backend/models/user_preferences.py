from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class UserPreferences:
    """Preferences saved from previous interactions."""

    preferred_brand: str | None = None
    preferred_transmission: str | None = None
    max_price_tnd: int | None = None
    preferred_city: str | None = None
    preferred_fuel: str | None = None
    favorite_models: list[str] = field(default_factory=list)
