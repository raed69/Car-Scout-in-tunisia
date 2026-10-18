from __future__ import annotations

import threading
import webbrowser
from dataclasses import asdict
from uuid import UUID

import anthropic
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.config import DEFAULT_USER_ID, PROJECT_ROOT  # also loads .env
from backend.agent.answer_question import answer_question
from backend.agent.conversation_state import ConversationState
from backend.agent.steps.load_conversation import load_chat_for_page
from backend.agent.steps.load_preferences import load_preferences
from backend.services.claude import ClaudeRefusedError, explain_error

# Only this computer can open the page: there is no login, so it must not be shared on a network.
HOST = "127.0.0.1"
PORT = 8000
# The React page, built by "npm run build" in the frontend folder.
BUILT_PAGE = PROJECT_ROOT / "frontend" / "dist"
NOT_BUILT = (
    "<p>The chat page is not built yet. In a terminal, go to the <code>frontend</code> folder and run "
    "<code>npm install</code> then <code>npm run build</code>. Then reload this page.</p>"
)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    conversation_id: UUID | None = None


def create_app() -> FastAPI:
    """Build the web app: one chat page and the routes it calls."""

    app = FastAPI(title="Car Scout")
    app.mount("/assets", StaticFiles(directory=BUILT_PAGE / "assets", check_dir=False), name="assets")

    @app.get("/", include_in_schema=False)
    def chat_page():
        page = BUILT_PAGE / "index.html"
        if not page.exists():
            return HTMLResponse(NOT_BUILT, status_code=503)
        return FileResponse(page)

    @app.get("/api/preferences")
    def get_preferences():
        state = load_preferences(ConversationState())
        return {"preferences": asdict(state.user_preferences), "warnings": state.storage_warnings}

    @app.get("/api/conversations/{conversation_id}")
    def get_conversation(conversation_id: UUID):
        """The messages of one chat, so the page can show it again after a reload."""

        try:
            messages = load_chat_for_page(str(conversation_id), DEFAULT_USER_ID)
        except requests.RequestException as error:
            return {"messages": [], "warnings": [f"Could not load the earlier messages: {error}"]}
        return {"messages": messages, "warnings": []}

    @app.post("/api/ask")
    def ask(request: AskRequest):
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=422, detail="Type a question first.")

        conversation_id = str(request.conversation_id) if request.conversation_id else None
        try:
            state = answer_question(question, conversation_id)
        except (ClaudeRefusedError, anthropic.APIError) as error:
            raise HTTPException(status_code=502, detail=explain_error(error)) from error

        return {
            "answer": state.final_answer or "",
            "conversation_id": state.conversation_id,
            "preferences": asdict(state.user_preferences),
            "warnings": state.storage_warnings,
        }

    return app


def run_web():
    """Start the web app on this computer and open it in the browser."""

    url = f"http://{HOST}:{PORT}"
    print(f"Car Scout is running at {url}. Press Ctrl+C here to stop it.")
    threading.Timer(1.0, webbrowser.open, [url]).start()
    uvicorn.run(create_app(), host=HOST, port=PORT, log_level="warning")


if __name__ == "__main__":
    run_web()
