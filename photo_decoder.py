import base64
import mimetypes
import subprocess
from pathlib import Path
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

def choose_image_file() -> Path:
    """Open the native macOS file picker."""
    result = subprocess.run(
        ["osascript", "-e", 'POSIX path of (choose file with prompt "Choose an image")'],
        capture_output=True,
        text=True,
    )
    filename = result.stdout.strip() if result.returncode == 0 else ""

    if not filename:
        raise SystemExit("No image selected.")

    return Path(filename).expanduser()

def image_to_data_url(image_path: Path) -> str:
    image_path = image_path.expanduser().resolve()

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Not an image file: {image_path}")

    image_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{image_b64}"

def build_image_message(image_path: Path, prompt) -> HumanMessage:
    return HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}},
        ]
    )


