from __future__ import annotations

from backend.agent.conversation_state import ConversationState
from backend.models.car_search import CarSearch
from backend.tools.search_car_ads import search_car_ads


def run_tools(state: ConversationState) -> ConversationState:
    """Execute the actual tool calls and record results."""

    search = search_car_ads(state.car_search or CarSearch())
    status = "failed" if "error" in search else "completed"
    state.last_tool_results.append({"type": "search", "status": status, **search})
    state.messages.append({"role": "assistant", "content": "Tool execution completed."})
    return state
