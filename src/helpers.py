import json
from pathlib import Path

def read_json(filepath: str | Path) -> dict:
    """Reads a `.json` file contents."""
    content = {"posts": []}
    with open(Path(filepath), "r") as file:
        content: dict = json.load(file)
    return content

def write_json(filepath: str | Path, content: dict) -> None:
    """Writes a dictionary to a `.json` file."""
    with open(Path(filepath), "w") as file:
        json.dump(content, file, indent=2)