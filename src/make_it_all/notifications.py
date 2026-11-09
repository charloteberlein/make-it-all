from dataclasses import dataclass
from datetime import date, datetime

from make_it_all.helpers import DATA_DIR, read_json
from make_it_all.pages.account.user import User

TASKS_JSON_PATH = DATA_DIR / "tasks.json"
DUE_SOON_DAYS = 3

# user id --> ids of the notifications they have read
read_ids: dict[int, set[str]] = {}

@dataclass
class Notification:
    id: str
    message: str
    task_type: str
    read: bool = False


def get_notifications(user: User) -> list[Notification]:
    # Returns a message for each of the user's unfinished tasks that is overdue or due soon (only lasts until the app closes)
    notifications = []
    today = date.today()
    user_read_ids = read_ids.get(user.id, set())

    for task in read_json(TASKS_JSON_PATH):
        person = task.get("owner") or task.get("assignees")
        if person != user.name or "Complete" in task["status"]:
            continue

        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        days_left = (due_date - today).days

        if days_left < 0:
            kind, text = "overdue", "Overdue"
        elif days_left <= DUE_SOON_DAYS:
            kind, text = "due-soon", "Due soon"
        else:
            continue

        notification_id = f"{kind}:{task['task_name']}:{task['due_date']}"
        name = task["task_name"]
        if len(name) > 35:
            name = name[:32] + "..."
        message = f"{text}: {name} (due {task['due_date']})"
        notifications.append(Notification(notification_id, message, task["type"], notification_id in user_read_ids))

    return notifications

def mark_all_read(user: User) -> None:
    # Marks every current notification for the user as read
    read_ids.setdefault(user.id, set()).update(n.id for n in get_notifications(user))