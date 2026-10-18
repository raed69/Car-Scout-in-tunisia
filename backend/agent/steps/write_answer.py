from __future__ import annotations

import json

from backend.agent.conversation_state import ConversationState
from backend.agent.load_prompt import load_prompt
from backend.agent.steps.load_conversation import format_earlier_messages
from backend.services.claude import ClaudeClient


def write_answer(state: ConversationState) -> ConversationState:
    """Create the final answer for the user."""

    user_message = next(
        (message["content"] for message in reversed(state.messages) if message["role"] == "user"),
        "",
    )
    search = state.last_tool_results[-1] if state.last_tool_results else {"results": []}
    request = (
        f"User message:\n{user_message}\n\n"
        f"Search results:\n{json.dumps(search, ensure_ascii=False, indent=2)}"
    )
    earlier = format_earlier_messages(state)
    if earlier:
        request = f"Earlier in this conversation:\n{earlier}\n\n{request}"

    state.final_answer = ClaudeClient().write(load_prompt("write_answer"), request)
    state.messages.append({"role": "assistant", "content": state.final_answer})
    return state
