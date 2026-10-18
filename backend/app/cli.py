from __future__ import annotations

import sys
from uuid import uuid4

import anthropic

import backend.config  # noqa: F401  (loads .env)
from backend.agent.answer_question import answer_question
from backend.services.claude import ClaudeRefusedError, explain_error


def run_cli():
    """Minimal command-line runner for the agent."""

    # Windows terminals default to an encoding that cannot print Arabic.
    sys.stdout.reconfigure(encoding="utf-8")

    print("Car Scout. Ask about a used car in Tunisia. Press Enter on an empty line to quit.")
    # Every question asked in this run is saved under the same conversation.
    conversation_id = str(uuid4())
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question or question.lower() in {"exit", "quit"}:
            break

        try:
            state = answer_question(question, conversation_id)
            print(f"\nCar Scout: {state.final_answer or ''}")
            for warning in state.storage_warnings:
                print(f"\n[Not saved] {warning}")
        except (ClaudeRefusedError, anthropic.APIError) as error:
            print(f"\nCar Scout: {explain_error(error)}")


if __name__ == "__main__":
    run_cli()
