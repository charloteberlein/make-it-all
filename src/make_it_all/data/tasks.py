import json

from make_it_all.data.json_store import DATA_DIR, read_json, write_json

TASKS_FILE = DATA_DIR / "tasks.json"

def load_tasks() -> list[dict]:
    try:
        return read_json(TASKS_FILE)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks: list[dict]) -> None:
    write_json(TASKS_FILE, tasks)
