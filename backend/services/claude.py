from __future__ import annotations

import os
from typing import TypeVar

import anthropic
from pydantic import BaseModel

from backend.config import DEFAULT_MODEL

# Lets the API retry on another model if a safety filter declines a request.
FALLBACK_BETA = "server-side-fallback-2026-07-01"
MAX_OUTPUT_TOKENS = 16000

Schema = TypeVar("Schema", bound=BaseModel)


class ClaudeRefusedError(RuntimeError):
    """Raised when Claude declines to answer a request."""


def explain_error(error: Exception) -> str:
    """Turn a Claude failure into a short message the user can act on."""

    if isinstance(error, anthropic.AuthenticationError):
        return "The Anthropic API key was rejected. Check ANTHROPIC_API_KEY in .env."
    if isinstance(error, anthropic.RateLimitError):
        return "Too many requests to Claude right now. Wait a minute and try again."
    if isinstance(error, anthropic.APIStatusError):
        return f"Claude returned an error ({error.status_code}): {error.message}"
    if isinstance(error, anthropic.APIConnectionError):
        return "Could not reach Claude. Check your internet connection."
    return str(error)


class ClaudeClient:
    """Thin wrapper around the Anthropic/Claude integration."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model or DEFAULT_MODEL
        self._client: anthropic.Anthropic | None = None

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def build_system_prompt(self, prompt_text: str) -> str:
        return prompt_text

    def _get_client(self) -> anthropic.Anthropic:
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    def _fallback_options(self) -> dict:
        # Haiku models have no server-side fallback, so the options are only sent for the others.
        if "haiku" in self.model:
            return {}
        return {"betas": [FALLBACK_BETA], "fallbacks": "default"}

    def extract(self, system: str, user_message: str, schema: type[Schema]) -> Schema:
        """Ask Claude to fill a structured model from free text."""

        response = self._get_client().beta.messages.parse(
            model=self.model,
            max_tokens=MAX_OUTPUT_TOKENS,
            system=system,
            messages=[{"role": "user", "content": user_message}],
            output_format=schema,
            output_config={"effort": "low"},
            **self._fallback_options(),
        )
        if response.stop_reason == "refusal" or response.parsed_output is None:
            raise ClaudeRefusedError("Claude did not return a structured result.")
        return response.parsed_output

    def write(self, system: str, user_message: str) -> str:
        """Ask Claude for a plain text reply."""

        response = self._get_client().beta.messages.create(
            model=self.model,
            max_tokens=MAX_OUTPUT_TOKENS,
            system=system,
            messages=[{"role": "user", "content": user_message}],
            output_config={"effort": "medium"},
            **self._fallback_options(),
        )
        if response.stop_reason == "refusal":
            raise ClaudeRefusedError("Claude declined to answer this request.")
        return "".join(block.text for block in response.content if block.type == "text").strip()
