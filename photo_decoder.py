import base64
import mimetypes
import subprocess
import tempfile
from pathlib import Path
from langchain.messages import HumanMessage

# Claude accepts these image types, up to ~5MB per image (base64-encoded)
SUPPORTED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_IMAGE_BYTES = 3_500_000  # raw bytes; base64 adds ~33%, keeping us under 5MB
MAX_DIMENSION = 1568  # larger images get downscaled by the API anyway


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


def prepare_image(image_path: Path) -> tuple[bytes, str]:
    """Return (bytes, mime_type), converting/shrinking with macOS `sips` when needed
    (e.g. iPhone HEIC photos or images over the size limit)."""
    image_path = image_path.expanduser().resolve()

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Not an image file: {image_path}")

    data = image_path.read_bytes()
    if mime_type in SUPPORTED_MIME_TYPES and len(data) <= MAX_IMAGE_BYTES:
        return data, mime_type

    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / "image.jpg"
        result = subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80",
             "-Z", str(MAX_DIMENSION), str(image_path), "--out", str(out_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not out_path.is_file():
            raise ValueError(f"Could not convert image {image_path}: {result.stderr.strip()}")
        return out_path.read_bytes(), "image/jpeg"


def build_image_message(image_path: Path, prompt) -> HumanMessage:
    data, mime_type = prepare_image(image_path)
    return HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image",
                "base64": base64.b64encode(data).decode("utf-8"),
                "mime_type": mime_type,
            },
        ]
    )
