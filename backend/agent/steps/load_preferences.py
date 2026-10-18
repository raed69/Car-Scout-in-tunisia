from __future__ import annotations

from dataclasses import fields

import requests

from backend.agent.conversation_state import ConversationState
from backend.services.supabase import SupabaseClient
from backend.models.user_preferences import UserPreferences
from backend.tools.save_preferences import PREFERENCES_TABLE


def load_preferences(state: ConversationState) -> ConversationState:
    """Load any saved preferences from a previous interaction."""

    state.user_preferences = UserPreferences()
    try:
        rows = SupabaseClient().select(PREFERENCES_TABLE, {"user_id": state.user_id})
    except requests.RequestException as error:
        state.storage_warnings.append(f"Could not load preferences: {error}")
        return state

    if rows:
        known = {item.name for item in fields(UserPreferences)}
        saved = {name: value for name, value in rows[0].items() if name in known and value is not None}
        state.user_preferences = UserPreferences(**saved)
        state.messages.append({"role": "system", "content": "Loaded saved preferences."})
    return state
