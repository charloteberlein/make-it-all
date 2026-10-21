import json
from pathlib import Path

def read_json(filepath: str | Path) -> dict:
    """Reads a .json file contents."""
    content = {"posts": []}
    with open(Path(filepath), "r") as file:
        content: dict = json.load(file)
    return content

def write_json(filepath: str | Path, content: str) -> None:
    """Writes to a .json file (placeholder)."""
    pass