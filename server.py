import logging
import tempfile
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chef import detect_ingredients, find_recipe, ask_chef

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

app = FastAPI(title="FastEat")


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
