# FastEat_Agent
A LangChain-based personal chef agent: snap a photo of your ingredients and it finds a recipe you can cook with them, then lets you refine it in a follow-up chat.

## How it works
1. You pick a photo (macOS file picker, or pass a path).
2. Claude identifies the ingredients in the image.
3. The agent searches the web (Tavily) for a matching recipe and returns it with ingredients, steps, and what you're missing.
4. Ask follow-ups like "make it vegetarian" or "I don't have an oven" — the conversation is remembered.

HEIC and large photos are converted/shrunk automatically with macOS `sips`.

## Setup
```bash
uv sync
```
Create a `.env` file:
```
ANTHROPIC_API_KEY=...
TAVILY_API_KEY=...
```

## Usage
```bash
uv run main.py                  # opens the file picker
uv run main.py ~/Desktop/fridge.jpg
```
Press Enter (or type `q`) to quit the follow-up chat.
