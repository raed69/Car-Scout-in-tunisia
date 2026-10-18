from __future__ import annotations


def compare_cars(items: list[dict]):
    """Minimal comparison routine used to rank cars by price, fuel economy, and age."""

    def score(item):
        price = float(item.get("price_tnd", 0))
        year = int(item.get("year", 2000) or 2000)
        age_penalty = max(0, 2026 - year) * 250
        return price + age_penalty

    ranked = sorted(items, key=score)
    return ranked
