from __future__ import annotations

import requests

from backend.config import MAX_SEARCH_RESULTS
from backend.services.searxng import SearxngClient
from backend.models.car_search import CarSearch
from backend.tools.read_ads import add_ad_details


def build_search_query(criteria: CarSearch) -> str:
    """Turn structured criteria into a web query aimed at Tunisian used-car ads."""

    parts = [
        criteria.brand,
        criteria.model,
        "occasion",
        criteria.fuel,
        criteria.transmission,
        criteria.city or "Tunisie",
    ]
    return " ".join(part for part in parts if part)


def search_car_ads(criteria: CarSearch):
    """Tool-like function for searching car listings by criteria."""

    query = build_search_query(criteria)
    output = {
        "criteria": criteria.model_dump(exclude_none=True, exclude={"needs_more_info", "follow_up_question"}),
        "query": query,
        "results": [],
        "source": "searxng",
    }

    try:
        output["results"] = SearxngClient().search(query, max_results=MAX_SEARCH_RESULTS)["results"]
    except requests.RequestException as error:
        output["error"] = f"SearXNG search failed: {error}"
        return output

    normal_range = add_ad_details(output["results"], criteria.max_price_tnd)
    if normal_range:
        output["normal_price_range_tnd"] = normal_range
    return output
