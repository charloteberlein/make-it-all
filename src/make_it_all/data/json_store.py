import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def read_json(filepath: str | Path) -> Any:
    """Read the contents of a JSON file."""
    with open(Path(filepath), "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(filepath: str | Path, content: Any) -> None:
    """Write JSON data to a file."""
    with open(Path(filepath), "w", encoding="utf-8") as file:
        json.dump(content, file, indent=2, ensure_ascii=False)
