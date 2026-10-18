from __future__ import annotations

import requests

from backend.config import MAX_SEARCH_RESULTS
from backend.services.searxng import SearxngClient
from backend.models.car_search import CarSearch


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
        "criteria": criteria.model_dump(exclude_none=True),
        "query": query,
        "results": [],
        "source": "searxng",
    }

    try:
        output["results"] = SearxngClient().search(query, max_results=MAX_SEARCH_RESULTS)["results"]
    except requests.RequestException as error:
        output["error"] = f"SearXNG search failed: {error}"

    return output
