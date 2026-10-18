from __future__ import annotations

from dataclasses import asdict

import requests

from backend.agent.conversation_state import ConversationState
from backend.models.user_preferences import UserPreferences
from backend.tools.save_preferences import save_preferences

# CarSearch field -> UserPreferences field
REMEMBERED_FIELDS = {
    "brand": "preferred_brand",
    "transmission": "preferred_transmission",
    "max_price_tnd": "max_price_tnd",
    "city": "preferred_city",
    "fuel": "preferred_fuel",
}


def remember_preferences(state: ConversationState) -> ConversationState:
    """Update the saved preferences with what the user asked for in this message."""

    if state.car_search is None:
        return state

    preferences = state.user_preferences or UserPreferences()
    before = asdict(preferences)
    for search_field, preference_field in REMEMBERED_FIELDS.items():
        value = getattr(state.car_search, search_field)
        if value is not None:
            setattr(preferences, preference_field, value)
    model = state.car_search.model
    if model and model not in preferences.favorite_models:
        preferences.favorite_models.append(model)
    state.user_preferences = preferences

    if asdict(preferences) != before:
        try:
            save_preferences(state.user_id, asdict(preferences))
        except requests.RequestException as error:
            state.storage_warnings.append(f"Could not save preferences: {error}")
    return state
