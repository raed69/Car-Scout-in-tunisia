from __future__ import annotations

import json
import re
from urllib.parse import urlparse

from backend.agent.conversation_state import ConversationState
from backend.agent.load_prompt import load_prompt
from backend.agent.steps.load_conversation import format_earlier_messages
from backend.services.claude import ClaudeClient

# One chosen ad in Claude's answer: "#3 | Best price for its age".
PICK_LINE = re.compile(r"^\s*#(\d+)\s*\|?\s*(.*)$")


def results_for_claude(search: dict) -> dict:
    """The search as Claude sees it: each result gets an id to pick it by, and no picture address."""

    results = [
        {"id": number, **{name: value for name, value in result.items() if name != "thumbnail"}}
        for number, result in enumerate(search.get("results", []), start=1)
    ]
    return {**search, "results": results}


def build_card(result: dict, note: str) -> dict:
    """What the chat page shows for one ad: picture, title, link, and what Car Scout read from it."""

    url = result.get("url", "")
    return {
        "url": url,
        "title": result.get("title", ""),
        "image": result.get("thumbnail"),
        "site": (urlparse(url).hostname or "").removeprefix("www."),
        "note": note,
        **result.get("details", {}),
    }


def split_answer(answer: str, results: list[dict]) -> tuple[str, list[dict]]:
    """Separate Claude's short text from its "#id | note" picks, and turn the picks into cards."""

    text_lines, cards, used = [], [], set()
    for line in answer.splitlines():
        match = PICK_LINE.match(line)
        if not match:
            text_lines.append(line)
            continue
        number = int(match.group(1))
        if 1 <= number <= len(results) and number not in used:
            used.add(number)
            cards.append(build_card(results[number - 1], match.group(2).strip()))
    return "\n".join(text_lines).strip(), cards


def write_answer(state: ConversationState) -> ConversationState:
    """Create the final answer for the user."""

    user_message = next(
        (message["content"] for message in reversed(state.messages) if message["role"] == "user"),
        "",
    )
    search = state.last_tool_results[-1] if state.last_tool_results else {"results": []}
    request = (
        f"User message:\n{user_message}\n\n"
        f"Search results:\n{json.dumps(results_for_claude(search), ensure_ascii=False, indent=2)}"
    )
    earlier = format_earlier_messages(state)
    if earlier:
        request = f"Earlier in this conversation:\n{earlier}\n\n{request}"

    answer = ClaudeClient().write(load_prompt("write_answer"), request)
    state.answer_text, state.car_cards = split_answer(answer, search.get("results", []))
    # The saved and remembered answer keeps the links as text, for the terminal chat and the next questions.
    links = [f"- {card['note'] or card['title']}: {card['url']}" for card in state.car_cards]
    state.final_answer = "\n".join([state.answer_text, *links]).strip()
    state.messages.append({"role": "assistant", "content": state.final_answer})
    return state
