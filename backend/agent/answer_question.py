from __future__ import annotations

from backend.agent.conversation_state import ConversationState
from backend.agent.steps.load_conversation import load_conversation
from backend.agent.steps.load_preferences import load_preferences
from backend.agent.steps.remember_preferences import remember_preferences
from backend.agent.steps.run_tools import run_tools
from backend.agent.steps.save_conversation import save_conversation
from backend.agent.steps.understand_message import understand_message
from backend.agent.steps.write_answer import write_answer


def answer_question(question: str, conversation_id: str | None = None) -> ConversationState:
    """Run one question through the agent steps and return the finished state."""

    state = ConversationState()
    if conversation_id:
        state.conversation_id = conversation_id
    state.messages.append({"role": "user", "content": question})
    load_preferences(state)
    if conversation_id:
        load_conversation(state)
    understand_message(state, question)
    remember_preferences(state)
    run_tools(state)
    write_answer(state)
    save_conversation(state)
    return state
