from __future__ import annotations

from datetime import date


def compare_cars(items: list[dict]):
    """Rank cars from best to worst value: a lower price is better, and each year of age costs 250 TND."""

    this_year = date.today().year

    def score(item):
        price = float(item.get("price_tnd", 0))
        year = int(item.get("year", 2000) or 2000)
        age_penalty = max(0, this_year - year) * 250
        return price + age_penalty

    ranked = sorted(items, key=score)
    return ranked
