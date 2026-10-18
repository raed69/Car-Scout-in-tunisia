from __future__ import annotations

import os

import requests

DEFAULT_SEARXNG_URL = "http://localhost:8080"


class SearxngClient:
    """Thin wrapper around a self-hosted SearXNG instance (no API key needed)."""

    def __init__(self, base_url: str | None = None, timeout: float = 15):
        self.base_url = (base_url or os.getenv("SEARXNG_URL") or DEFAULT_SEARXNG_URL).rstrip("/")
        self.timeout = timeout

    def is_configured(self) -> bool:
        return bool(self.base_url)

    def search(self, query: str, max_results: int = 5):
        response = requests.get(
            f"{self.base_url}/search",
            params={"q": query, "format": "json"},
            timeout=self.timeout,
        )
        response.raise_for_status()

        results = [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "engine": item.get("engine"),
            }
            for item in response.json().get("results", [])[:max_results]
        ]
        return {"query": query, "results": results, "max_results": max_results}
