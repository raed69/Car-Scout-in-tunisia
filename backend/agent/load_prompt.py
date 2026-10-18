from __future__ import annotations

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def load_prompt(name: str) -> str:
    """Return the main instructions followed by the prompt for one step."""

    main = (PROMPTS_DIR / "main_instructions.md").read_text(encoding="utf-8")
    step = (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")
    return f"{main}\n\n{step}"
