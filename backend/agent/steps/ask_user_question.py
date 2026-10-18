from __future__ import annotations

from backend.agent.conversation_state import ConversationState

DEFAULT_QUESTION = "Which car are you looking for (brand or model), and what is your budget?"


def ask_user_question(state: ConversationState) -> ConversationState:
    """Answer with one short question when the request is too vague to search."""

    question = (state.car_search.follow_up_question if state.car_search else None) or DEFAULT_QUESTION
    state.needs_more_info = True
    state.final_answer = question
    state.messages.append({"role": "assistant", "content": question})
    return state
