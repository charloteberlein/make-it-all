from pathlib import Path
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"

def generate_id() -> str:
    """Generates a random UUID."""
    return str(uuid4())
