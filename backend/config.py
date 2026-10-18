from pathlib import Path

import truststore
from dotenv import load_dotenv

# Use the Windows certificate store so HTTPS works behind antivirus SSL scanning.
truststore.inject_into_ssl()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
MAX_TOOL_CALLS = 8
# Haiku is the cheapest model. For better answers at a higher price, use "claude-opus-5-5".
DEFAULT_MODEL = "claude-haiku-5-5"
# The CLI has no login, so everything is saved under this one user.
DEFAULT_USER_ID = "local_user"

# Guardrail values to keep the agent predictable and bounded.
MAX_SEARCH_RESULTS = 10
# How much of the chat is sent back to Claude with each new question. More means better
# follow-ups but a slightly higher price per question.
MAX_EARLIER_MESSAGES = 10
MAX_EARLIER_MESSAGE_LENGTH = 1500
MAX_EXPLANATION_LENGTH = 600
