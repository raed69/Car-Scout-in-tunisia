from __future__ import annotations

from backend.agent.conversation_state import ConversationState


def ask_user_question(state: ConversationState) -> ConversationState:
    """Ask one targeted follow-up question when the request is incomplete."""

    state.needs_more_info = True
    state.messages.append({"role": "assistant", "content": "What is your budget and preferred city?"})
    return state
