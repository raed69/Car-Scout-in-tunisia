from __future__ import annotations

import json

from backend.agent.conversation_state import ConversationState
from backend.agent.load_prompt import load_prompt
from backend.agent.steps.load_conversation import format_earlier_messages
from backend.services.claude import ClaudeClient
from backend.models.car_search import CarSearch

# CarSearch field -> UserPreferences field. Brand and models are left out on purpose:
# a saved brand must never be added to a request for a different car.
DEFAULT_FIELDS = {
    "fuel": "preferred_fuel",
    "transmission": "preferred_transmission",
    "city": "preferred_city",
    "max_price_tnd": "max_price_tnd",
}


def build_request(state: ConversationState, message: str) -> str:
    """Put the saved preferences and the earlier messages, if any, in front of the user's message."""

    preferences = state.user_preferences
    saved = {
        search_field: getattr(preferences, preference_field)
        for search_field, preference_field in DEFAULT_FIELDS.items()
        if preferences is not None and getattr(preferences, preference_field) is not None
    }
    earlier = format_earlier_messages(state)
    if not saved and not earlier:
        return message

    sections = []
    if saved:
        sections.append(f"Saved preferences:\n{json.dumps(saved, ensure_ascii=False)}")
    if earlier:
        sections.append(f"Earlier in this conversation:\n{earlier}")
    sections.append(f"User message:\n{message}")
    return "\n\n".join(sections)


def understand_message(state: ConversationState, user_message: str | None = None) -> ConversationState:
    """Extract the search intent and fill the structured CarSearch model."""

    message = user_message or (state.messages[-1]["content"] if state.messages else "")
    state.car_search = ClaudeClient().extract(
        load_prompt("understand_message"), build_request(state, message), CarSearch
    )
    state.user_goal = "search_cars"
    state.messages.append({"role": "assistant", "content": "Request has been structured."})
    return state
