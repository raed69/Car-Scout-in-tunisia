from __future__ import annotations

from backend.agent.conversation_state import ConversationState


def think_and_use_tools(state: ConversationState) -> ConversationState:
    """Decide which tools are required to answer the request."""

    state.tool_calls_so_far += 1
    state.messages.append({"role": "assistant", "content": "I will search ads and validate fair pricing."})
    return state
