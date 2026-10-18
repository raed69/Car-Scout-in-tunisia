from __future__ import annotations

from backend.agent.conversation_state import ConversationState
from backend.config import MAX_TOOL_CALLS


def choose_next_step(state: ConversationState) -> str:
    """Route the workflow to the appropriate next node."""

    if state.needs_more_info:
        return "ask_user_question"
    if state.car_search is None:
        return "understand_message"
    if state.tool_calls_so_far < MAX_TOOL_CALLS:
        return "think_and_use_tools"
    return "write_answer"
