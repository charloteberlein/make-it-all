from collections import defaultdict
from datetime import date, datetime

from make_it_all.pages.todos.task_status import TaskStatus, parse_task_status


def _project_tasks(tasks):
    return [task for task in tasks if task.get("type", "project") == "project"]


def _involved_in_task(task, user_name):
    if user_name is None or len(user_name) == "":
        return True
    if task["assigner"] == user_name:
        return True

    assignees = task.get("assignees", "")
    return user_name in assignees.split(", ")


def calc_project_completion_percentages(tasks):
    """Calculates percentage progress for each project depending on number of 'completed' tasks."""
    project_tasks = _project_tasks(tasks)
    project_stats = defaultdict(lambda: {"total": 0, "completed": 0})  # Initialise

    for task in project_tasks:
        project_title = task.get("project_name", "General").strip()
        if not project_title:
            project_title = "General"
        project_stats[project_title]["total"] += 1
        if parse_task_status(task.get("status")) is TaskStatus.COMPLETED:
            project_stats[project_title]["completed"] += 1

    percentages = {}
    for project, data in project_stats.items():
        total = data["total"]
        completed = data["completed"]
        percent = (completed / total * 100) if total > 0 else 0
        percentages[project] = {
            "percentage": round(percent, 1),
            "completed": completed,
            "total": total,
        }
    return percentages


def calc_project_task_status_counts(tasks, user_name=None):
    """Counts awaiting-info, in-progress, and completed project tasks by project."""
    project_counts = defaultdict(
        lambda: {
            TaskStatus.AWAITING_INFO: 0,
            TaskStatus.IN_PROGRESS: 0,
            TaskStatus.COMPLETED: 0,
        }
    )

    for task in _project_tasks(tasks):
        if not _involved_in_task(task, user_name):
            continue

        project_name = task.get("project_name", "General").strip() or "General"
        status = parse_task_status(task.get("status"))
        if status in project_counts[project_name]:
            project_counts[project_name][status] += 1

    return dict(project_counts)


def calc_employee_task_status_counts(tasks, user_name=None):
    """Counts each employee's assigned project tasks by status."""
    employee_counts = defaultdict(
        lambda: {
            TaskStatus.AWAITING_INFO: 0,
            TaskStatus.IN_PROGRESS: 0,
            TaskStatus.COMPLETED: 0,
        }
    )

    for task in _project_tasks(tasks):
        if not _involved_in_task(task, user_name):
            continue

        assignees = task.get("assignees", "")
        if isinstance(assignees, list):
            assignee_list = [
                str(assignee).strip() for assignee in assignees if str(assignee).strip()
            ]
        else:
            assignee_list = [
                assignee.strip() for assignee in str(assignees).split(",") if assignee.strip()
            ]

        status = parse_task_status(task.get("status"))
        if status not in (TaskStatus.AWAITING_INFO, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED):
            continue
        for employee in assignee_list:
            employee_counts[employee][status] += 1

    return dict(employee_counts)


def get_emp_tasks(tasks):
    """Gathers all the current tasks each employee is working on."""
    project_tasks = _project_tasks(tasks)
    emp_data = defaultdict(lambda: {"completed": [], "active": []})

    for task in project_tasks:
        assignees = task.get("assignees", "")
        if isinstance(assignees, list):
            assignee_list = [a.strip() for a in assignees if a.strip()]
        else:
            assignee_list = [a.strip() for a in str(assignees).split(",") if a.strip()]

        status = parse_task_status(task.get("status"))

        for emp in assignee_list:
            if status is TaskStatus.COMPLETED:
                emp_data[emp]["completed"].append(task)
            elif status in (TaskStatus.IN_PROGRESS, TaskStatus.AWAITING_INFO):
                emp_data[emp]["active"].append(task)

    return emp_data


def calc_task_completion_times(task):
    """Calculates how many tasks an employee has finished on time and if they are late."""
    due_str = task.get("due_date", "")
    comp_str = task.get("completion_date", "")
    status = parse_task_status(task.get("status"))

    if status is TaskStatus.SUSPENDED:
        return None

    if not due_str:
        return "No due date set for this task."

    try:
        due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
    except ValueError:
        return None

    if status is TaskStatus.COMPLETED and comp_str:
        try:
            comp_date = datetime.strptime(comp_str, "%Y-%m-%d").date()
            return (due_date - comp_date).days
        except ValueError:
            return None

    if status in (TaskStatus.IN_PROGRESS, TaskStatus.AWAITING_INFO):
        today = date.today()
        return (due_date - today).days

    return None


def calc_project_hours(tasks):
    """Calculates the efficiency of each project, using estimated and actual amount of time."""
    project_tasks = _project_tasks(tasks)
    project_hours = defaultdict(lambda: {"total_estimated": 0.0, "total_actual": 0.0})

    for task in project_tasks:
        project_title = task.get("project_name", "General").strip()
        if not project_title:
            project_title = "General"

        try:
            estimate_t = float(task.get("estimated_time", 0.0))
        except (ValueError, TypeError):
            estimate_t = 0.0

        try:
            actual_t = float(task.get("actual_time", 0.0))
        except (ValueError, TypeError):
            actual_t = 0.0

        project_hours[project_title]["total_estimated"] += estimate_t
        project_hours[project_title]["total_actual"] += actual_t

    details = {}
    grand_estimate = 0.0
    grand_actual = 0.0

    for project, data in project_hours.items():
        estimate_t = data["total_estimated"]
        actual_t = data["total_actual"]

        grand_estimate += estimate_t
        grand_actual += actual_t

        # Calculates efficiency percentage for a given project.
        if actual_t > 0:
            efficiency = round((estimate_t / actual_t) * 100, 1)
        else:
            efficiency = 100.0 if estimate_t == 0 else 0.0

        details[project] = {
            "total_estimated": estimate_t,
            "total_actual": actual_t,
            "efficiency": efficiency,
        }

    overall_efficiency = (
        round((grand_estimate / grand_actual) * 100, 1)
        if grand_actual > 0
        else (100.0 if grand_estimate == 0 else 0.0)
    )

    overall_summary = {
        "total_estimated": grand_estimate,
        "total_actual": grand_actual,
        "efficiency": overall_efficiency,
    }

    return {"details": details, "summary": overall_summary}


def calc_emp_hours_summary(tasks):
    project_tasks = _project_tasks(tasks)
    emp_hours = defaultdict(lambda: {"total_estimated": 0.0, "total_actual": 0.0})

    for task in project_tasks:
        assignees = task.get("assignees", "")
        if isinstance(assignees, list):
            assignee_list = [a.strip() for a in assignees if a.strip()]
        else:
            assignee_list = [a.strip() for a in str(assignees).split(",") if a.strip()]

        if not assignee_list:
            continue

        try:
            estimate_t = float(task.get("estimated_time", 0.0))
        except (ValueError, TypeError):
            estimate_t = 0.0

        try:
            actual_t = float(task.get("actual_time", 0.0))
        except (ValueError, TypeError):
            actual_t = 0.0

        # Split hours evenly among assignees to keep individual workloads accurate => can be more complex in Part 2.
        num_assignees = len(assignee_list)
        est_per_person = estimate_t / num_assignees
        act_per_person = actual_t / num_assignees

        for emp in assignee_list:
            emp_hours[emp]["total_estimated"] += est_per_person
            emp_hours[emp]["total_actual"] += act_per_person

    return dict(emp_hours)
