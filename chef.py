"""Agent + schemas for the web app. The shapes here match the data contract in
fasteat-design-handoff/DESIGN_HANDOFF.md."""
import base64
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from prompt import DETECT_PROMPT, WEB_CHEF_PROMPT
from tools import web_search
from photo_decoder import prepare_image

load_dotenv()

MODEL = "claude-haiku-5-5"


class DetectedIngredients(BaseModel):
    detected_ingredients: list[str]


class Ingredient(BaseModel):
    name: str
    qty: str
    have: bool
    substitute: str | None = None


class Recipe(BaseModel):
    title: str
    source_name: str
    source_url: str
    image_url: str | None = None
    time_minutes: int
    servings: int
    difficulty: str = Field(description="Easy, Medium or Hard")
    tags: list[str] = Field(description="Short labels like 'No oven' or 'Vegetarian'")
    ingredients: list[Ingredient]
    steps: list[str]


class Change(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    from_: str = Field(alias="from")
    to: str


class ChefReply(BaseModel):
    message: str
    recipe: Recipe | None = None
    changes: list[Change] = []


detector = init_chat_model(MODEL, model_provider="anthropic").with_structured_output(DetectedIngredients)

# one agent for both recipe search and chat; the checkpointer keeps each session's
# conversation under its own thread_id
agent = create_agent(model=f"anthropic:{MODEL}",
                     tools=[web_search],
                     system_prompt=WEB_CHEF_PROMPT,
                     response_format=ChefReply,
                     checkpointer=InMemorySaver())


def detect_ingredients(image_path: Path) -> tuple[list[str], str]:
    """Return (ingredients, preview data URL). The preview is the JPEG/PNG we sent to Claude,
    so the browser can show it even when the upload was HEIC."""
    data, mime_type = prepare_image(image_path)
    b64 = base64.b64encode(data).decode("utf-8")
    result = detector.invoke([HumanMessage(content=[
        {"type": "text", "text": DETECT_PROMPT},
        {"type": "image", "base64": b64, "mime_type": mime_type},
    ])])
    return result.detected_ingredients, f"data:{mime_type};base64,{b64}"


def ask_chef(session_id: str, text: str) -> ChefReply:
    response = agent.invoke({"messages": [HumanMessage(text)]},
                            {"configurable": {"thread_id": session_id}})
    return response["structured_response"]


def find_recipe(session_id: str, ingredients: list[str], preferences: list[str], another: bool) -> ChefReply:
    text = f"My ingredients: {', '.join(ingredients)}."
    if preferences:
        text += f"\nPreferences: {', '.join(preferences)}."
    text += ("\nFind me a different recipe from the ones you suggested before." if another
             else "\nFind me a recipe.")
    return ask_chef(session_id, text)
