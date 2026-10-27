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
        self.load_tasks()
        self.current_user: User | None = None
        super().__init__()

    def showEvent(self, event):
        # Grabs current user from Main Window on page load.
        super().showEvent(event)
        main_window = self.window()
        if hasattr(main_window, "current_user"):
            self.current_user = main_window.current_user

    def define_layout(self) -> None:
        # Projects bar layout
        self.projects_bar_layout = QHBoxLayout()
        self.projects_bar_layout.setSpacing(5)
        self.projects_bar_frame = QFrame()

        # Main vertical layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(20)

    def define_widgets(self) -> None:
        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.switch_to_dashboard.emit)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    
        # Define the buttons for each project
        self.project1 = QPushButton("Project 1")
        self.project1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.project1.setObjectName("project1Button")

        self.project2 = QPushButton("Project 2")
        self.project2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.project2.setObjectName("project2Button")

        self.project3 = QPushButton("Project 3")
        self.project3.setCursor(Qt.CursorShape.PointingHandCursor)
        self.project3.setObjectName("project3Button")

        self.projects_tabs = []
        for task in self.tasks:
            task_name = QLabel(task.get("task_name", "Unknown task"))
            status = QLabel(task.get("status", ""))
            due_date = QLabel(task.get("due_date", "YYYY-MM-DD"))

            name = task.get("task_name", "Unknown task")
            if len(name) > 10:
                name = name[:10] + "..."
            project_btn = QPushButton(name)
            project_btn.setObjectName("LoginButton")
            #project_btn.clicked.connect()
            if (
                self.current_user is not None
                and self.current_user.rank != "Manager"
                and task.get("assigner", "") != self.current_user.name
            ):
                project_btn.hide()

            self.projects_tabs.append(project_btn)
                
    def assemble_widgets(self) -> None:
        # Add buttons to horizontal layout
        self.projects_bar_layout.addWidget(self.back_btn)
        for tab in self.projects_tabs:
            self.projects_bar_layout.addWidget(tab)
        self.projects_bar_frame.setLayout(self.projects_bar_layout)

        self.layout.addWidget(self.projects_bar_frame)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def load_tasks(self):
        try:
            self.tasks = read_json(TASKS_FILE)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []