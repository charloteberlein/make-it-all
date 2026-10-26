import json
from pathlib import Path
from uuid import uuid4

def read_json(filepath: str | Path) -> dict | list:
    """Reads a `.json` file contents."""
    content = {"posts": []}
    with open(Path(filepath), "r", encoding = "utf-8") as file:
        content: dict = json.load(file)
    return content

def write_json(filepath: str | Path, content: dict | list) -> None:
    """Writes a dictionary to a `.json` file."""
    with open(Path(filepath), "w", encoding = "utf-8") as file:
        json.dump(content, file, indent=2, ensure_ascii = False)

def generate_id() -> str:
    """Generates a random UUID."""
    return str(uuid4())
