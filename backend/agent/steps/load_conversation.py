from __future__ import annotations

import requests

from backend.agent.conversation_state import ConversationState
from backend.agent.steps.save_conversation import MESSAGES_TABLE
from backend.config import MAX_EARLIER_MESSAGE_LENGTH, MAX_EARLIER_MESSAGES
from backend.services.supabase import SupabaseClient


def load_conversation(state: ConversationState) -> ConversationState:
    """Load the last questions and answers of this chat, so a follow-up question is understood."""

    try:
        rows = SupabaseClient().select(
            MESSAGES_TABLE,
            {"conversation_id": state.conversation_id, "user_id": state.user_id},
            order="id.desc",
            limit=MAX_EARLIER_MESSAGES,
        )
    except requests.RequestException as error:
        state.storage_warnings.append(f"Could not load the earlier messages: {error}")
        return state

    # Long answers are cut, because the whole chat is sent to Claude again with every question.
    state.earlier_messages = [
        {"role": row["role"], "content": row["content"][:MAX_EARLIER_MESSAGE_LENGTH]}
        for row in reversed(rows)
    ]
    return state


def format_earlier_messages(state: ConversationState) -> str:
    """Write the earlier messages as a short transcript, or return "" for a new chat."""

    names = {"user": "User", "assistant": "Car Scout"}
    return "\n\n".join(f"{names[message['role']]}: {message['content']}" for message in state.earlier_messages)
