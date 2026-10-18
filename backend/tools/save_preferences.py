from __future__ import annotations

from datetime import datetime, timezone

from backend.services.supabase import SupabaseClient

PREFERENCES_TABLE = "user_preferences"


def save_preferences(user_id: str, preferences: dict):
    """Persist a user's preferences to the user_preferences table in Supabase."""

    row = {
        **preferences,
        "user_id": user_id,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    SupabaseClient().upsert(PREFERENCES_TABLE, row, key_column="user_id")
    return {"saved_to": PREFERENCES_TABLE, "preferences": preferences}
