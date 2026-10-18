from __future__ import annotations

import os

import requests


class SupabaseClient:
    """Thin wrapper around the Supabase REST API for reading and writing table rows."""

    def __init__(self, project_url: str | None = None, api_key: str | None = None, timeout: float = 15):
        self.project_url = (project_url or os.getenv("SUPABASE_PROJECT_URL") or "").rstrip("/")
        # The secret key is for trusted code like this app; the publishable key only works
        # on tables that have a policy allowing it.
        self.api_key = api_key or os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")
        self.timeout = timeout

    def is_configured(self) -> bool:
        return bool(self.project_url and self.api_key)

    def _request(self, method: str, table: str, prefer: str | None = None, **kwargs) -> requests.Response:
        if not self.is_configured():
            raise requests.RequestException("SUPABASE_PROJECT_URL or the Supabase key is missing in .env.")

        headers = {"apikey": self.api_key, "Authorization": f"Bearer {self.api_key}"}
        if prefer:
            headers["Prefer"] = prefer
        response = requests.request(
            method,
            f"{self.project_url}/rest/v1/{table}",
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )
        if not response.ok:
            raise requests.HTTPError(f"Supabase returned {response.status_code}: {response.text}", response=response)
        return response

    def select(
        self,
        table: str,
        filters: dict[str, str] | None = None,
        order: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Return the rows where every column in filters equals the given value.

        order is a column name, with ".desc" for the newest or largest first, such as "id.desc".
        """

        params = {column: f"eq.{value}" for column, value in (filters or {}).items()}
        if order:
            params["order"] = order
        if limit:
            params["limit"] = limit
        return self._request("GET", table, params=params).json()

    def insert(self, table: str, rows: list[dict]) -> None:
        self._request("POST", table, prefer="return=minimal", json=rows)

    def upsert(self, table: str, row: dict, key_column: str) -> None:
        """Insert the row, or update the existing row that has the same key."""

        self._request(
            "POST",
            table,
            prefer="resolution=merge-duplicates,return=minimal",
            params={"on_conflict": key_column},
            json=row,
        )
