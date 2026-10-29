from enum import Enum

class TaskStatus(Enum):
    IN_PROGRESS = "⏳ In Progress"
    AWAITING_INFO = "💬 Awaiting Info"
    COMPLETED = "✅ Complete"
    SUSPENDED = "❌ Suspended"

def parse_task_status(value: str) -> TaskStatus:
    """Converts stored or displayed status labels to the shared task-status enum."""
    status = str(value).lower()
    if "awaiting info" in status:
        return TaskStatus.AWAITING_INFO
    if "in progress" in status:
        return TaskStatus.IN_PROGRESS
    if "complete" in status:
        return TaskStatus.COMPLETED
    if "suspended" in status:
        return TaskStatus.SUSPENDED
    return TaskStatus.IN_PROGRESS

def task_status_options() -> list[str]:
    return [status.value for status in TaskStatus]
