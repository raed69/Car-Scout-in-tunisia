from __future__ import annotations

import requests

from backend.agent.conversation_state import ConversationState
from backend.services.supabase import SupabaseClient

MESSAGES_TABLE = "conversation_messages"


def save_conversation(state: ConversationState) -> ConversationState:
    """Store the user's question and the final answer in Supabase."""

    question = next(
        (message["content"] for message in reversed(state.messages) if message["role"] == "user"),
        None,
    )
    rows = [
        {
            "conversation_id": state.conversation_id,
            "user_id": state.user_id,
            "role": role,
            "content": content,
        }
        for role, content in (("user", question), ("assistant", state.final_answer))
        if content
    ]
    if not rows:
        return state

    try:
        SupabaseClient().insert(MESSAGES_TABLE, rows)
    except requests.RequestException as error:
        state.storage_warnings.append(f"Could not save the conversation: {error}")
    return state
