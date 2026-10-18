# Car Scout

Car Scout is an agentic AI project for the Tunisian car market. It helps users search, compare, and evaluate used cars in Darija, French, or English.

## Project structure

```
CarScout/
  main.py          starts the app
  frontend/        the chat page, built with React and Vite
    src/App.jsx    the page: messages, sending a question
    src/components/  Header, Welcome, Message, Composer (the text box)
    src/api.js     the calls to the backend
  backend/         all the Python code
    config.py      settings, loads .env
    agent/         the agent steps and the prompts sent to Claude
    tools/         tools the agent uses: ad search, saving preferences
    services/      connections to Claude, SearXNG and Supabase
    models/        the shapes of the data: a search, an ad, preferences
    rules/         price check and car comparison
    app/           the web API (api.py) and the terminal chat (cli.py)
  setup/           files used once to set things up
    database/      tables to create in Supabase
    searxng/       SearXNG settings
```

## Quick start

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment variables:
   ```bash
   copy .env.example .env
   ```
4. Build the chat page (React). This needs Node.js. Run it once, and again after each change to the `frontend` folder:
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```
5. Start the chat page:
   ```bash
   python main.py
   ```
   It opens `http://127.0.0.1:8000` in your browser. Press Ctrl+C in the terminal to stop it. The page only works on this computer, because it has no login.

   While working on the page, run `python main.py` in one terminal and `npm run dev` in the `frontend` folder in a second terminal, then open the address Vite prints (usually `http://localhost:5173`). The page updates as soon as you save a file, without building again.

   To chat in the terminal instead:
   ```bash
   python main.py cli
   ```

## Environment variables

Set any API keys in `.env` before using real integrations.

Web search uses a local SearXNG container (no API key). It reads its settings from `setup/searxng/settings.yml`, which must keep `json` in `search.formats`. That file is not on GitHub because it holds a secret key: copy `settings.example.yml` to `settings.yml` and put a random string in `secret_key`. Then start the container:

```bash
docker run -d --name searxng -p 8080:8080 -v "%cd%\setup\searxng:/etc/searxng" searxng/searxng
```

Set `SEARXNG_URL` if it runs somewhere other than `http://localhost:8080`.

Conversations and preferences are saved in Supabase. Run `setup/database/create_tables.sql` once in the Supabase SQL Editor, then set `SUPABASE_PROJECT_URL` and `SUPABASE_SECRET_KEY` in `.env`. If Supabase cannot be reached, Car Scout still answers and prints a `[Not saved]` warning.

## Notes

This seed project is intentionally structured to match the project guide and is ready for deeper implementation of the search, comparison, and pricing flow.
