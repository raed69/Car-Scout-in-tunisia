from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SearchResult:
    """Normalized result returned by a search tool."""

    query: str
    results: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class ToolCallOutcome:
    """Outcome to be logged by the agent after a tool call."""

    name: str
    success: bool
    message: str
    data: dict | None = None
