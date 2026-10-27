import json
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QLabel

from pages.base_page import BasePage
from pages.account.user import User
from helpers import read_json

TASKS_FILE = "assets/mock_data/tasks.json"


class DashboardView(BasePage):
    switch_to_dashboard = Signal()

    def __init__(self):
        self.tasks = []
        self._current_user: User | None = None
        self.projects_details = dict()
        super().__init__()

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, user: User | None):
        self._current_user = user

        if self._current_user is not None and self._current_user.rank == "Team Lead":
            self.tasks = self.get_tasks_for_team_lead()
        else:
            self.tasks = self.load_tasks()

    def showEvent(self, event):
        # Grabs current user from Main Window on page load.
        super().showEvent(event)
        main_window = self.window()

        if hasattr(main_window, "current_user"):
            self.current_user = main_window.current_user

        self.refresh_project_task_tables()

    def define_layout(self) -> None:
        # Title layout
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(10, 0, 10, 0)
        self.title_layout.setSpacing(5)
        self.title_frame = QFrame()

        # Main vertical layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(20)

        self.tables_layout = QVBoxLayout()
        self.tables_layout.setSpacing(16)
        self.tables_frame = QFrame()

    def define_widgets(self) -> None:
        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.switch_to_dashboard.emit)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setToolTip("Back to progress overview")

        self.title_label = QLabel("Task overview")
        self.title_label.setObjectName("TitleLabel")
                
    def assemble_widgets(self) -> None:
        self.title_layout.addWidget(self.back_btn)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.title_layout.addStretch()
        self.title_frame.setLayout(self.title_layout)

        self.tables_frame.setLayout(self.tables_layout)

        self.layout.addWidget(self.title_frame)
        self.layout.addWidget(self.tables_frame)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def load_tasks(self):
        try:
            tasks = read_json(TASKS_FILE)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = []
        return tasks

    def get_tasks_for_team_lead(self) -> list[dict]:
        return [
            task
            for task in self.load_tasks()
            if task.get("type") == "project"
            and task.get("assigner") == (
                self.current_user.name
                if self.current_user is not None
                else ""
            )
        ]

    def group_tasks_by_employee_assigned(self, tasks: list[dict]) -> dict[str, list[dict]]:
        employee_tasks: dict[str, list[dict]] = {}

        for task in tasks:
            employee_names = str(task.get("assignees", "")).split(",")

            if not employee_names:
                employee_names = ["Unassigned"]

            for employee_name in employee_names:
                if employee_name not in employee_tasks:
                    employee_tasks[employee_name] = [task]
                else:
                    employee_tasks[employee_name].append(task)

        return employee_tasks

    def get_project_task_tables(self) -> list[QFrame]:
        project_tasks = [task for task in self.tasks if task.get("type") == "project"]
        self.projects_details = self.group_tasks_by_employee_assigned(project_tasks)

        employee_frames = []
        for (employee_name, details) in self.projects_details.items():
            employee_label = QLabel(employee_name)
            employee_label.setObjectName("PostTitle")

            employee_table_layout = QVBoxLayout()
            employee_table_layout.setContentsMargins(0, 0, 0, 0)
            employee_table_layout.setSpacing(0)
            employee_table_layout.addWidget(employee_label)
            employee_table_frame = QFrame()

            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(0)
            for heading in ("Task", "Status", "Due date"):
                heading_label = QLabel(heading)
                heading_label.setObjectName("TaskTableHeader")
                header_layout.addWidget(heading_label)
            header_frame = QFrame()
            header_frame.setLayout(header_layout)
            employee_table_layout.addWidget(header_frame)

            for detail in details:
                employee_row_layout = QHBoxLayout()
                employee_row_layout.setContentsMargins(0, 0, 0, 0)
                employee_row_layout.setSpacing(0)
                employee_row_frame = QFrame()

                task_name_label = QLabel(detail.get("task_name", "Unknown task"))
                status_label = QLabel(detail.get("status", ""))
                due_date_label = QLabel(detail.get("due_date", "YYYY-MM-DD"))

                for label in (task_name_label, status_label, due_date_label):
                    label.setObjectName("TaskTable")

                employee_row_layout.addWidget(task_name_label)
                employee_row_layout.addWidget(status_label)
                employee_row_layout.addWidget(due_date_label)
                employee_row_frame.setLayout(employee_row_layout)

                employee_table_layout.addWidget(employee_row_frame)

            employee_table_frame.setLayout(employee_table_layout)
            employee_frames.append(employee_table_frame)

        return employee_frames

    def refresh_project_task_tables(self) -> None:
        while self.tables_layout.count():
            item = self.tables_layout.takeAt(0)
            widget = item.widget() if item is not None else None
            if widget is not None:
                widget.deleteLater()

        frames = self.get_project_task_tables()
        if not frames:
            self.tables_layout.addWidget(QLabel("No project tasks to display."))
            return

        for frame in frames:
            self.tables_layout.addWidget(frame)