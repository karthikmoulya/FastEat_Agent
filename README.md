# FastEat_Agent
A LangChain-based personal chef agent: snap a photo of your ingredients and it finds a recipe you can cook with them, then lets you refine it in a follow-up chat.

Comes as a **web app** (React + FastAPI) and a **command-line** version.

## How it works
1. You upload a photo (or type your ingredients).
2. Claude identifies the ingredients; you fix anything it missed and pick preferences (Vegetarian, Under 30 min, No oven, Spicy).
3. The agent searches the web (Tavily) for a matching recipe and shows what you have and what's missing, with substitutes.
4. Ask follow-ups like "make it vegan" — the chef proposes changes you can apply to the recipe.

HEIC and large photos are converted/shrunk automatically with Pillow.

## Project layout
| File | What it does |
|---|---|
| `server.py` | FastAPI app: `/api/detect`, `/api/recipe`, `/api/chat`; also serves the built frontend |
| `chef.py` | The web agent and the JSON schemas the UI uses |
| `prompt.py` | System prompts |
| `tools.py` | Tavily web search tool |
| `photo_decoder.py` | Image loading/conversion |
| `main.py` | Command-line version |
| `frontend/` | React app (Vite) |
| `fasteat-design-handoff/` | Design mockups and spec |

## Setup
```bash
uv sync
cd frontend && npm install
```
Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=...
TAVILY_API_KEY=...
```

## Run the web app
Development (two terminals, hot reload):
```bash
uv run uvicorn server:app --reload --port 8000   # backend
cd frontend && npm run dev                       # frontend → http://localhost:5173
```
Or build once and serve everything from FastAPI:
```bash
cd frontend && npm run build && cd ..
uv run uvicorn server:app --port 8000            # → http://localhost:8000
```

## Deploy to Render (free)
The repo includes a `Dockerfile` (builds the React app, then runs FastAPI) and a `render.yaml` blueprint.
1. Sign in at [render.com](https://render.com) with GitHub.
2. **New → Blueprint**, pick this repo.
3. Enter `ANTHROPIC_API_KEY` and `TAVILY_API_KEY` when asked (paste the raw key, no quotes).
4. Deploy. Every push to `main` redeploys.

The free plan sleeps after 15 minutes idle (first visit then takes ~1 minute) and chat memory resets on restart.
To protect your API bill, the server limits each visitor to 30 requests/hour and everyone to 300/day
(change with the `RATE_LIMIT_PER_HOUR` / `RATE_LIMIT_PER_DAY` env vars). Also set a monthly spend limit in the Anthropic Console.

Test the production build locally with Docker:
```bash
docker build -t fasteat .
set -a; source .env; set +a
docker run -p 10000:10000 -e PORT=10000 -e ANTHROPIC_API_KEY -e TAVILY_API_KEY fasteat
```

## Run the command-line version
```bash
uv run main.py                  # opens the file picker
uv run main.py ~/Desktop/fridge.jpg
```
