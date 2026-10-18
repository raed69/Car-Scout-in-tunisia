from __future__ import annotations

import requests

from backend.agent.conversation_state import ConversationState
from backend.agent.steps.save_conversation import MESSAGES_TABLE
from backend.config import MAX_EARLIER_MESSAGE_LENGTH, MAX_EARLIER_MESSAGES
from backend.services.supabase import SupabaseClient

# The page shows at most this many messages of an old chat.
MAX_MESSAGES_SHOWN = 200


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


def load_chat_for_page(conversation_id: str, user_id: str) -> list[dict]:
    """Return every message of one chat, oldest first, so the page can show it again after a reload.

    Raises requests.RequestException when Supabase cannot be reached.
    """

    rows = SupabaseClient().select(
        MESSAGES_TABLE,
        {"conversation_id": conversation_id, "user_id": user_id},
        order="id.asc",
        limit=MAX_MESSAGES_SHOWN,
    )
    return [{"role": row["role"], "content": row["content"]} for row in rows]


def format_earlier_messages(state: ConversationState) -> str:
    """Write the earlier messages as a short transcript, or return "" for a new chat."""

    names = {"user": "User", "assistant": "Car Scout"}
    return "\n\n".join(f"{names[message['role']]}: {message['content']}" for message in state.earlier_messages)
