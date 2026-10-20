import logging
import os
import tempfile
import time
from collections import defaultdict, deque
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chef import detect_ingredients, find_recipe, ask_chef

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

app = FastAPI(title="FastEat")

# Rate limits protect the Anthropic/Tavily bill once the app is public.
# In memory, so they reset when the server restarts — fine for a single free instance.
PER_VISITOR_PER_HOUR = int(os.getenv("RATE_LIMIT_PER_HOUR", "30"))
TOTAL_PER_DAY = int(os.getenv("RATE_LIMIT_PER_DAY", "300"))
visitor_calls: dict[str, deque] = defaultdict(deque)
all_calls: deque = deque()


def over_limit(calls: deque, limit: int, window_seconds: int, now: float) -> bool:
    while calls and calls[0] < now - window_seconds:
        calls.popleft()
    return len(calls) >= limit


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.method == "POST" and request.url.path.startswith("/api/"):
        # Render sits behind a proxy, so the real visitor IP is in X-Forwarded-For
        forwarded = request.headers.get("x-forwarded-for", "")
        visitor = forwarded.split(",")[0].strip() or (request.client.host if request.client else "unknown")
        now = time.time()
        if over_limit(all_calls, TOTAL_PER_DAY, 24 * 3600, now):
            return JSONResponse({"detail": "FastEat has hit its daily limit. Please try again tomorrow."}, status_code=429)
        if over_limit(visitor_calls[visitor], PER_VISITOR_PER_HOUR, 3600, now):
            return JSONResponse({"detail": "You're cooking a lot! Please wait a bit and try again."}, status_code=429)
        visitor_calls[visitor].append(now)
        all_calls.append(now)
    return await call_next(request)


@app.get("/api/health")
def health():
    return {"ok": True}


class RecipeRequest(BaseModel):
    session_id: str
    ingredients: list[str]
    preferences: list[str] = []
    another: bool = False


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/api/detect")
def detect(photo: UploadFile):
    suffix = Path(photo.filename or "").suffix or ".jpg"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / f"upload{suffix}"
        path.write_bytes(photo.file.read())
        try:
            ingredients, preview = detect_ingredients(path)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"detected_ingredients": ingredients, "preview": preview}


@app.post("/api/recipe")
def recipe(req: RecipeRequest):
    if not req.ingredients:
        raise HTTPException(status_code=400, detail="Add at least one ingredient.")
    reply = find_recipe(req.session_id, req.ingredients, req.preferences, req.another)
    return reply.model_dump(by_alias=True)


@app.post("/api/chat")
def chat(req: ChatRequest):
    return ask_chef(req.session_id, req.message).model_dump(by_alias=True)


# serve the built React app (npm run build) from the same server
dist = Path(__file__).parent / "frontend" / "dist"
if dist.is_dir():
    app.mount("/", StaticFiles(directory=dist, html=True), name="frontend")
