from __future__ import annotations

try:
    from langgraph.graph import StateGraph
except ImportError:  # pragma: no cover
    StateGraph = None

from backend.agent.choose_next_step import choose_next_step
from backend.agent.conversation_state import ConversationState
from backend.agent.steps.ask_user_question import ask_user_question
from backend.agent.steps.load_preferences import load_preferences
from backend.agent.steps.run_tools import run_tools
from backend.agent.steps.think_and_use_tools import think_and_use_tools
from backend.agent.steps.understand_message import understand_message
from backend.agent.steps.write_answer import write_answer


def build_agent():
    """Build the LangGraph workflow used by the agent."""

    if StateGraph is None:
        return {
            "status": "not_ready",
            "message": "Install the project dependencies to activate the graph workflow.",
        }

    workflow = StateGraph(ConversationState)
    workflow.add_node("load_preferences", load_preferences)
    workflow.add_node("understand_message", lambda state: understand_message(state, state.messages[-1]["content"]) if state.messages else state)
    workflow.add_node("ask_user_question", ask_user_question)
    workflow.add_node("think_and_use_tools", think_and_use_tools)
    workflow.add_node("run_tools", run_tools)
    workflow.add_node("write_answer", write_answer)

    workflow.set_entry_point("load_preferences")
    workflow.add_edge("load_preferences", "understand_message")
    workflow.add_conditional_edges(
        "understand_message",
        choose_next_step,
        {
            "ask_user_question": "ask_user_question",
            "understand_message": "understand_message",
            "think_and_use_tools": "think_and_use_tools",
            "write_answer": "write_answer",
        },
    )
    workflow.add_edge("ask_user_question", "understand_message")
    workflow.add_edge("think_and_use_tools", "run_tools")
    workflow.add_edge("run_tools", "think_and_use_tools")
    workflow.add_edge("run_tools", "write_answer")
    workflow.add_edge("write_answer", "__end__")

    return workflow.compile()
