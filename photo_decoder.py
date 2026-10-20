import base64
import io
import subprocess
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener
from langchain.messages import HumanMessage

register_heif_opener()  # lets Pillow open iPhone HEIC photos

# Claude accepts these image types, up to ~5MB per image (base64-encoded)
SUPPORTED_FORMATS = {"JPEG": "image/jpeg", "PNG": "image/png", "GIF": "image/gif", "WEBP": "image/webp"}
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
    """Return (bytes, mime_type), converting to a resized JPEG when needed
    (e.g. iPhone HEIC photos or images over the size limit)."""
    image_path = image_path.expanduser().resolve()

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    data = image_path.read_bytes()
    try:
        image = Image.open(io.BytesIO(data))
    except UnidentifiedImageError:
        raise ValueError(f"Not an image file: {image_path.name}")

    mime_type = SUPPORTED_FORMATS.get(image.format)
    if mime_type and len(data) <= MAX_IMAGE_BYTES:
        return data, mime_type

    image = ImageOps.exif_transpose(image)  # keep phone photos the right way up
    image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
    out = io.BytesIO()
    image.convert("RGB").save(out, format="JPEG", quality=80)
    return out.getvalue(), "image/jpeg"


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
