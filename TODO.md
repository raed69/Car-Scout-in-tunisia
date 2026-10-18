# Car Scout: what is missing

Status on 8 October 2026.

The project is a skeleton. The folders and files exist, but most parts are fake for now. Tick a box when a part is done.

## What already works

- [x] Web search through the local SearXNG container (free, no API key). Code: `backend/services/searxng.py` and `backend/tools/search_car_ads.py`.
- [x] The `.env` file is loaded when the app starts (`backend/config.py`).
- [x] Price check rules: cheap, fair or expensive (`backend/rules/price_evaluation.py`).
- [x] Saving preferences to Supabase (`backend/tools/save_preferences.py`).

## First version that really works

Done and tested with a real question on 10 October 2026. The sentences below describe how each part was before. You can now type a question, Claude understands it, searches SearXNG and answers with real links.

- [x] **1. Connect Claude.** `backend/services/claude.py` only stores the API key. It never sends a message to Claude.
- [x] **2. Understand the user's message with Claude.** `backend/agent/steps/understand_message.py` only looks for the words "golf", "diesel", "tunis" and "60k". Any other request is not understood.
- [x] **3. Make the agent use the real search.** `backend/agent/steps/run_tools.py` pretends to search and returns an empty list. It must call `search_car_ads`.
- [x] **4. Write a real answer.** `backend/agent/steps/write_answer.py` always prints the same sentence. Claude should write the answer from the search results, with links.
- [x] **5. Let the user type a question.** `backend/app/cli.py` has one question written inside the code.

## Next

- [ ] **6. Turn search results into real ads.** Written on 18 October 2026, waiting for a test with real questions. `backend/tools/read_ads.py` reads the price, year and mileage from each result's title and snippet (no Claude, so free). When at least 3 results show a price, each one is marked cheap, fair or expensive against the others (`market_range` in `backend/rules/price_evaluation.py`), over budget or not, and ranked by value (`compare_cars`). Checked on sample ad texts. Limit: it only sees the short snippet, not the full ad page.
- [x] **7. Save conversations and preferences in Supabase.** Tables `conversation_messages` and `user_preferences` (`setup/database/create_tables.sql`). Code: `backend/services/supabase.py`, `backend/agent/steps/load_preferences.py`, `remember_preferences.py`, `save_conversation.py`. Tested with a real question on 10 October 2026.
- [ ] **7b. Use the saved preferences.** The code is written: saved fuel, gearbox, city and budget fill in what a new message leaves out (`backend/agent/steps/understand_message.py` and its prompt), and the answer says what was assumed. Not yet tested with Claude.
- [ ] **8. Ask a real follow-up question.** Written on 18 October 2026, waiting for a test with real questions. When a request is too vague ("nheb karhba"), Claude sets `needs_more_info` and writes one short question (`backend/models/car_search.py` and the `understand_message` prompt). `backend/agent/answer_question.py` then answers with that question and skips the search and the second Claude call. It never asks twice in a row.
- [ ] **8b. Bring back the chat after a page reload.** Written on 18 October 2026, waiting for a test. The browser remembers the open chat (`frontend/src/App.jsx`), and the new route `/api/conversations/{id}` (`backend/app/api.py`) sends its messages back from Supabase. Checked without Claude on a saved chat.
- [ ] **9. Check the agent graph.** `backend/agent/build_agent.py` is never run by the CLI, and its steps loop without a clear way to stop.

## Smaller things

- [x] Update the model name in `backend/config.py`. It now uses `claude-haiku-5-5`, the cheapest model (switched from `claude-opus-5-5` on 10 October 2026 to save money; not yet tested with a real question).
- [ ] Real car specs. `backend/tools/get_car_specs.py` returns the same answer for every car.
- [x] Removed the old placeholder `actions/search_ads.py` (18 October 2026).
- [x] `backend/rules/compare_cars.py` uses the current year instead of 2026 written in the code (18 October 2026).
- [x] Web page and web API. `python main.py` opens the chat page (React, in `frontend/`, served by `backend/app/api.py`). `python main.py cli` keeps the terminal chat. Tested on 11 October 2026 with a fake answer, so no Claude credit was spent. Not yet tested with a real question.
- [x] **Remember earlier messages.** The code is written (18 October 2026): `backend/agent/steps/load_conversation.py` loads the last 10 messages of the chat from Supabase and gives them to Claude, so "and a cheaper one?" can be understood. Tested without Claude: the messages load in the right order. Tested with real questions on 18 October 2026: follow-ups work.
- [ ] Tests.
- [x] Git and GitHub: pushed to https://github.com/raed69/Car-Scout-in-tunisia on 18 October 2026. `.env` and `setup/searxng/settings.yml` (it has a secret key) stay on this computer only.

## How to start SearXNG

Open Docker Desktop, click **Containers**, and press the play button next to `searxng`. Or type `docker start searxng` in a terminal.
