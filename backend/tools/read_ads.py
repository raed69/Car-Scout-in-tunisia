from __future__ import annotations

import re
from datetime import date
from urllib.parse import urlparse

from backend.models.car_ad import CarAd
from backend.rules.compare_cars import compare_cars
from backend.rules.price_evaluation import assess_price, market_range

# A number written like "45000", "45 000", "45.000", "45,000" or "4.5".
NUMBER = r"(\d{1,3}(?:[ .,  ]\d{3})+|\d+(?:[.,]\d+)?)"
# Words that mean "thousand": "45k", "45 mille", "45md" (mille dinars), "45 alf", "45 ألف".
THOUSAND = r"(k|mille|md|m\.d|alf|ألف)"
CURRENCY = r"(dt|tnd|dinars?|د\.?ت|دينار)"
NOT_KM = r"(?!\s*(?:km|kilom|كلم))"

# "45 000 DT", "45md", "45 mille dinars". "120 mille km" is a mileage, not a price.
PRICE_WITH_UNIT = re.compile(rf"{NUMBER}\s*(?:{THOUSAND}\s*)?{CURRENCY}?\b{NOT_KM}", re.IGNORECASE)
# "prix: 45000", "soum 45": a number right after a word that means price.
PRICE_AFTER_WORD = re.compile(rf"\b(?:prix|price|soum|سعر)\s*:?\s*{NUMBER}\s*{THOUSAND}?{NOT_KM}", re.IGNORECASE)
MILEAGE = re.compile(rf"{NUMBER}\s*{THOUSAND}?\s*(?:km|kms|kilom|كلم)", re.IGNORECASE)
# A year on its own, not inside a date like 03/02/2020 or a longer number.
YEAR = re.compile(r"(?<![\d/\-.,])(19[6-9]\d|20[0-4]\d)(?![\d/\-]|[.,]\d)")

LOWEST_PRICE_TND = 2_000
HIGHEST_PRICE_TND = 1_500_000
HIGHEST_MILEAGE_KM = 800_000


def to_number(text: str) -> float:
    """Read "45 000", "45.000" or "4,5" as a number."""

    text = re.sub(r"[   ]", "", text)
    if re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", text):
        return float(re.sub(r"[.,]", "", text))
    return float(text.replace(",", "."))


def read_price(text: str) -> int | None:
    """Find a price in TND. A number counts only when a currency or "thousand" word goes with it."""

    candidates = []
    for match in PRICE_WITH_UNIT.finditer(text):
        number, thousand, currency = match.groups()
        if thousand or currency:
            candidates.append(to_number(number) * (1000 if thousand else 1))
    for match in PRICE_AFTER_WORD.finditer(text):
        value = to_number(match.group(1))
        if match.group(2) or value < 1000:
            value *= 1000
        candidates.append(value)

    for value in candidates:
        if LOWEST_PRICE_TND <= value <= HIGHEST_PRICE_TND:
            return int(value)
    return None


def read_mileage(text: str) -> int | None:
    for match in MILEAGE.finditer(text):
        value = to_number(match.group(1)) * (1000 if match.group(2) else 1)
        if value <= HIGHEST_MILEAGE_KM:
            return int(value)
    return None


def read_year(text: str) -> int | None:
    latest = date.today().year + 1
    for match in YEAR.finditer(text):
        year = int(match.group(1))
        if 1960 <= year <= latest:
            return year
    return None


def read_ad(result: dict) -> CarAd:
    """Read the price, year and mileage from a search result's title and snippet."""

    title = result.get("title", "")
    text = f"{title} \n {result.get('content', '')}"
    url = result.get("url") or None
    return CarAd(
        title=title,
        url=url,
        price_tnd=read_price(text),
        year=read_year(text),
        mileage_km=read_mileage(text),
        source=urlparse(url).hostname if url else None,
    )


def add_ad_details(results: list[dict], max_price_tnd: int | None = None) -> list[int] | None:
    """Add a "details" entry to each search result: price, year, mileage and a price check.

    The price check compares each price with the other prices found in the same search,
    so it only appears when at least 3 results show a price. Returns that normal price
    range as [low, high], or None.
    """

    ads = [read_ad(result) for result in results]
    priced = [{"index": i, "price_tnd": ad.price_tnd, "year": ad.year} for i, ad in enumerate(ads) if ad.price_tnd]
    expected = market_range([item["price_tnd"] for item in priced])
    value_rank = {item["index"]: rank for rank, item in enumerate(compare_cars(priced), start=1)}

    for index, (result, ad) in enumerate(zip(results, ads)):
        details = {
            "price_tnd": ad.price_tnd,
            "year": ad.year,
            "mileage_km": ad.mileage_km,
        }
        if ad.price_tnd and expected:
            details["price_check"] = assess_price(ad.price_tnd, expected).label
        if ad.price_tnd and max_price_tnd:
            details["over_budget"] = ad.price_tnd > max_price_tnd
        if index in value_rank and len(value_rank) > 1:
            details["value_rank"] = value_rank[index]
        result["details"] = {name: value for name, value in details.items() if value is not None}

    return [round(bound) for bound in expected] if expected else None
