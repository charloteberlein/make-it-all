from datetime import datetime, date
from helpers import read_json
from collections import defaultdict

TASKS_FILE = "assets/mock_data/tasks.json"

def calc_project_completion_percentages():
    """Calculates percentage progress for each project depending on number of 'completed' tasks."""
    tasks = read_json(TASKS_FILE)
    project_tasks = [t for t in tasks if t.get("type", "project") == "project"]
    project_stats = defaultdict(lambda: {"total": 0, "completed": 0}) # Initialise

    # project_title == project_name, just diff vars for clarity.
    for task in project_tasks:
        project_title = task.get("project_name", "General").strip()
        if not project_title:
            project_title = "General"

        project_stats[project_title]["total"] += 1
        status = task.get("status", "").lower()
        if "complete" in status:
            project_stats[project_title]["completed"] += 1

    percentages = {}
    for project, data in project_stats.items():
        total = data["total"]
        completed = data["completed"]
        percent = (completed / total * 100) if total > 0 else 0
        percentages[project] = {"percentage": round(percent, 1), "completed": completed, "total": total}
    return percentages

def get_emp_tasks():
    """Gathers all the current tasks each employee is working on."""
    tasks = read_json(TASKS_FILE)
    project_tasks = [t for t in tasks if t.get("type", "project") == "project"]
    emp_data = defaultdict(lambda: {"completed": [], "active": []})

    for task in project_tasks:
        assignees = task.get("assignees", "")
        if isinstance(assignees, list):
            assignee_list = [a.strip() for a in assignees if a.strip()]
        else:
            assignee_list = [a.strip() for a in str(assignees).split(",") if a.strip()]

        status = task.get("status", "").lower()
        is_completed = "complete" in status
        is_active = "in progress" in status or "awaiting info" in status
        
        for emp in assignee_list:
            if is_completed:
                emp_data[emp]["completed"].append(task)
            elif is_active:
                emp_data[emp]["active"].append(task)
                
    return emp_data

def calc_task_completion_times(task):
    """Calculates how many tasks an employee has finished on time and if they are late."""
    due_str = task.get("due_date", "")
    comp_str = task.get("completion_date", "")
    status = task.get("status", "").lower()

    if "suspended" in status:
        return None
    
    if not due_str:
        return "No due date set for this task."
    
    try:
        due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
    except ValueError:
        return None

    if "complete" in status and comp_str:
        try:
            comp_date = datetime.strptime(comp_str, "%Y-%m-%d").date()
            return (due_date - comp_date).days
        except ValueError:
            return None
            
    if "in progress" in status or "awaiting info" in status:
        today = date.today()
        return (due_date - today).days
        
    return None

def calc_project_hours():
    tasks = read_json(TASKS_FILE)
    project_tasks = [t for t in tasks if t.get("type", "project") == "project"]
    project_hours = defaultdict(lambda: {"total_estimated": 0.0, "total_actual": 0.0})

    for task in project_tasks:
        project_title = task.get("project_name", "General").strip()
        if not project_title:
            project_title = "General"

        try:
            est = float(task.get("estimated_time", 0.0))
        except (ValueError, TypeError):
            est = 0.0

        try:
            act = float(task.get("actual_time", 0.0))
        except (ValueError, TypeError):
            act = 0.0

        project_hours[project_title]["total_estimated"] += est
        project_hours[project_title]["total_actual"] += act

    details = {}
    grand_est = 0.0
    grand_act = 0.0

    for project, data in project_hours.items():
        est = data["total_estimated"]
        act = data["total_actual"]
        
        grand_est += est
        grand_act += act

        # Calculates efficiency percentage for a given project.
        if act > 0:
            efficiency = round((est / act) * 100, 1)
        else:
            efficiency = 100.0 if est == 0 else 0.0
            
        details[project] = {
            "total_estimated": est,
            "total_actual": act,
            "efficiency": efficiency
        }

    overall_efficiency = round((grand_est / grand_act) * 100, 1) if grand_act > 0 else (100.0 if grand_est == 0 else 0.0)
    
    overall_summary = {
        "total_estimated": grand_est,
        "total_actual": grand_act,
        "efficiency": overall_efficiency
    }

    return {
        "details": details,
        "summary": overall_summary
    }


def calc_emp_hours_summary():
    tasks = read_json(TASKS_FILE)
    project_tasks = [t for t in tasks if t.get("type", "project") == "project"]
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
            est = float(task.get("estimated_time", 0.0))
        except (ValueError, TypeError):
            est = 0.0

        try:
            act = float(task.get("actual_time", 0.0))
        except (ValueError, TypeError):
            act = 0.0

        # Split hours evenly among assignees to keep individual workloads accurate => can be more complex in Part 2.
        num_assignees = len(assignee_list)
        est_per_person = est / num_assignees
        act_per_person = act / num_assignees

        for emp in assignee_list:
            emp_hours[emp]["total_estimated"] += est_per_person
            emp_hours[emp]["total_actual"] += act_per_person

    return dict(emp_hours)