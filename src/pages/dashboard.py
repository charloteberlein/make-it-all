import json
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout, QProgressBar, QPushButton
from pages.base_page import BasePage
from helpers import read_json
from pages.todos.task_analytics import calc_project_completion_percentages, get_emp_tasks
from PySide6.QtCore import Signal, Qt

TASKS_FILE = "assets/mock_data/tasks.json"

class DashboardPage(BasePage):
    to_Training = Signal()

    def __init__(self, current_user=None):
        self.current_user = current_user
        super().__init__()
        self.load_tasks()
        self.populate_content()

    def showEvent(self, event):
        super().showEvent(event)
        main_window = self.window()
        if hasattr(main_window, "current_user") and main_window.current_user:
            self.current_user = main_window.current_user
        self.training_btn.setVisible(bool(self.current_user and self.current_user.rank in ["Manager", "Team Lead"]))
        self.load_tasks()
        self.populate_content()

    def get_current_user_name(self) -> str:
        if self.current_user and hasattr(self.current_user, "name"):
            return self.current_user.name
        return ""

    def define_widgets(self) -> None:
        user_name = self.get_current_user_name()

        self.titleLabel = QLabel(f"{user_name}'s Dashboard")
        self.titleLabel.setObjectName("HeadingLabel")

        self.progressTrackerHeader = QLabel("My Project Progress")
        self.progressTrackerHeader.setObjectName("SubheadingLabel")

        self.training_btn = QPushButton("▶️ To Training Page")
        self.training_btn.setObjectName("NavButton")
        self.training_btn.setCursor(Qt.PointingHandCursor)
        self.training_btn.setFixedWidth(200)
        self.training_btn.clicked.connect(self.to_Training.emit)

        self.progress_frame = QFrame()
        self.progress_frame.setObjectName("ProgFrame")
        self.progress_frame.setFrameShape(QFrame.Shape.Box)
        
        self.progress_layout = QVBoxLayout(self.progress_frame)

    def assemble_widgets(self) -> None:
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.titleLabel)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.training_btn)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.progressTrackerHeader)
        self.main_layout.addWidget(self.progress_frame)
        self.main_layout.addStretch(1)

        self.layout.addLayout(self.main_layout)
        self.setLayout(self.layout)

    def load_tasks(self):
        try:
            self.tasks = read_json(TASKS_FILE)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def populate_content(self):
        while self.progress_layout.count():
            item = self.progress_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        user_name = self.get_current_user_name()

        if user_name:
            self.titleLabel.setText(f"{user_name}'s Dashboard")

        all_percentages = calc_project_completion_percentages(TASKS_FILE)
        emp_data = get_emp_tasks(TASKS_FILE)

        user_projects = set()

        # Check assignee status with get_emp_tasks.
        if user_name in emp_data:
            user_tasks = emp_data[user_name]["completed"] + emp_data[user_name]["active"]
            for task in user_tasks:
                proj_name = task.get("project_name", "General").strip()
                if proj_name:
                    user_projects.add(proj_name)

        # Check assigner status across project tasks.
        for task in self.tasks:
            if task.get("type") == "project":
                assigner = str(task.get("assigner", "")).strip()
                if user_name and assigner.lower() == user_name.lower():
                    proj_name = task.get("project_name", "General").strip()
                    if proj_name:
                        user_projects.add(proj_name)

        # Filters all projects.
        if not user_name:
            filtered_stats = all_percentages
        else:
            filtered_stats = {
                proj: data for proj, data in all_percentages.items() 
                if proj in user_projects
            }

        if not filtered_stats:
            no_project_label = QLabel("You are currently assigned to no active projects.")
            self.progress_layout.addWidget(no_project_label)
            return

        # Renders progress bars.
        for project_name, data in filtered_stats.items():
            total = data["total"]
            completed = data["completed"]
            percent = data["percentage"]

            label = QLabel(f"{project_name} — {percent}% ({completed}/{total} completed)")
            
            bar = QProgressBar()
            bar.setValue(int(percent))
            bar.setFixedHeight(18)
            bar.setTextVisible(False)
            # Styles wouldn't be applied unless directly placed here.
            bar.setStyleSheet("""
                QProgressBar {
                    background-color: #c7c7c7;
                    border: 2px solid #334155;
                    border-radius: 6px;
                }
                QProgressBar::chunk {
                    background-color: #eab308;
                    border-radius: 4px;
                }
            """)

            self.progress_layout.addWidget(label)
            self.progress_layout.addSpacing(4)
            self.progress_layout.addWidget(bar)
            self.progress_layout.addSpacing(14)