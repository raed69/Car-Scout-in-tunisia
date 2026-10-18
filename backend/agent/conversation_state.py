from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from backend.config import DEFAULT_USER_ID
from backend.models.car_search import CarSearch
from backend.models.user_preferences import UserPreferences


@dataclass
class ConversationState:
    """The working state shared by all agent steps."""

    messages: list[dict] = field(default_factory=list)
    user_goal: str | None = None
    car_search: CarSearch | None = None
    user_preferences: UserPreferences | None = None
    needs_more_info: bool = False
    tool_calls_so_far: int = 0
    last_tool_results: list[dict] = field(default_factory=list)
    final_answer: str | None = None
    user_id: str = DEFAULT_USER_ID
    conversation_id: str = field(default_factory=lambda: str(uuid4()))
    storage_warnings: list[str] = field(default_factory=list)
