from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QPushButton, QProgressBar, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QFrame
)

from pages.base_page import BasePage
from pages.account.user import User

# TODO: Create a widget to show estimated percentage of time completed

class DashboardPage(BasePage):
    switch_to_signin = Signal()
    switch_to_training = Signal()
    switch_to_notifications = Signal()

    #Variables for testing - will be taken from to-do in future
    projectNum = 3
    projectName = "testing :)"
    progressValue = 23
    totalTime = 180
    timeTaken = 60
    timePercentage = int((timeTaken/totalTime) * 100)

    def __init__(self):
        self._current_user = None
        super().__init__()

    def showEvent(self, event):
        # Grabs current user from Main Window on page load.
        super().showEvent(event)
        main_window = self.window()
        if hasattr(main_window, "current_user"):
            self.current_user = main_window.current_user

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, user: User | None):
        self._current_user = user

        if self.current_user is not None:
            match self.current_user.rank:
                case "Manager":
                    self.view_employee_dashboard.setText("Manager Dashboard")
                    self.view_employee_dashboard.show()
                case "Team Lead":
                    self.view_employee_dashboard.setText("Employee Dashboard")
                    self.view_employee_dashboard.show()
                case _:
                    self.view_employee_dashboard.hide()
        else:
            self.view_employee_dashboard.hide()

    def define_layout(self) -> None:
        # Buttons
        self.navbar_layout = QHBoxLayout()
        self.navbar_layout.setSpacing(5)
        self.navbar_frame = QFrame()
    
        # Tasks
        self.overdue_frame = QFrame()
        self.overdue_frame.setFixedHeight(200)
        self.overdue_frame.setObjectName("TaskFrame")
        self.overdue_layout = QVBoxLayout()

        self.upcoming_frame = QFrame()
        self.upcoming_frame.setFixedHeight(200)
        self.upcoming_frame.setObjectName("TaskFrame")
        self.upcoming_layout = QVBoxLayout()

        self.completed_frame = QFrame()
        self.completed_frame.setFixedHeight(200)
        self.completed_frame.setObjectName("TaskFrame")
        self.completed_layout = QVBoxLayout()

        # Progress tracker
        self.progress_frame = QFrame()
        self.progress_frame.setObjectName("ProgressFrame")
        self.progress_frame.setFrameShape(QFrame.Shape.Box)
        self.progress_frame_layout = QVBoxLayout()

        # Progress bars
        self.progress_layout = QVBoxLayout()
        self.progress_layout.setContentsMargins(10, 10, 10, 10)
        self.progress_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Tasks
        self.task_layout = QHBoxLayout()
        self.task_layout.setSpacing(10)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(20)

    def define_widgets(self) -> None:
        # Navigation bar
        self.training = QPushButton("Training")
        self.training.setCursor(Qt.CursorShape.PointingHandCursor)
        self.training.setObjectName("LoginButton")
        self.training.clicked.connect(self.switch_to_training.emit)

        self.notifications = QPushButton("Notifications")
        self.notifications.setCursor(Qt.CursorShape.PointingHandCursor)
        self.notifications.setObjectName("LoginButton")
        self.notifications.clicked.connect(self.switch_to_notifications.emit)

        self.view_employee_dashboard = QPushButton("Employee Dashboard")
        self.view_employee_dashboard.setCursor(Qt.CursorShape.PointingHandCursor)
        self.view_employee_dashboard.setObjectName("LoginButton")

        # Default layout - no projects
        self.progress_tracker_header = QLabel("Progress Overview")
        self.progress_tracker_header.setObjectName("TitleLabelCenter")
        self.progress_tracker_header.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.no_projects_label = QLabel("No projects currently being tracked.")
        self.no_projects_label.setObjectName("noProjectLabel")
        self.no_projects_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.todo = QPushButton("To-Do List")
                
    def assemble_widgets(self) -> None:
        # Nav bar
        self.navbar_layout.addWidget(self.training)
        self.navbar_layout.addWidget(self.notifications)
        self.navbar_layout.addWidget(self.view_employee_dashboard)
        self.navbar_frame.setLayout(self.navbar_layout)

        # Progress
        self.progress_frame_layout.addWidget(self.progress_tracker_header)
        self.progress_frame.setLayout(self.progress_frame_layout)

        if self.projectNum <= 0:
            self.progress_frame_layout.addWidget(self.no_projects_label)
        else:
            for _ in range(self.projectNum):
                self.progress_frame_layout.addWidget(
                    self.create_progress_bar(
                        self.projectName, self.progressValue, self.timePercentage
                    )
                )

        # Tasks and progress
        # TODO: Add widgets
        self.overdue_frame.setLayout(self.overdue_layout)

        # TODO: Add widgets
        self.upcoming_frame.setLayout(self.upcoming_layout)

        # TODO: Add widgets
        self.completed_frame.setLayout(self.completed_layout)

        self.task_layout.addWidget(self.overdue_frame)
        self.task_layout.addWidget(self.upcoming_frame)
        self.task_layout.addWidget(self.completed_frame)

        # Main layout
        self.layout.addWidget(self.navbar_frame)
        self.layout.addWidget(self.progress_frame)
        self.layout.addStretch()
        self.layout.addLayout(self.task_layout)
        self.setLayout(self.layout)

    def create_progress_bar(self, project_name, progress_value, time_percentage):
        # Sub-layouts
        project_layout = QHBoxLayout()
        project_layout.setContentsMargins(10, 5, 10, 5)
        project_layout.setSpacing(10)
        project_frame = QFrame()

        progress_stack_layout = QVBoxLayout()
        progress_stack_layout.setContentsMargins(0, 0, 0, 0)
        progress_stack_layout.setSpacing(5)
        progress_stack_frame = QFrame()

        percentage_stack_layout = QVBoxLayout()
        percentage_stack_layout.setContentsMargins(0, 0, 0, 0)
        percentage_stack_layout.setSpacing(5)
        percentage_stack_frame = QFrame()

        # Project widgets
        project_label = QLabel(project_name)
        project_label.setObjectName("projectLabel")
        project_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        project_label.setFixedWidth(100)

        progressBar = QProgressBar()
        progressBar.setRange(0, 100)
        progressBar.setValue(progress_value)
        progressBar.setFixedHeight(15)
        progressBar.setTextVisible(False)

        elapsedTimeBar = QProgressBar()
        elapsedTimeBar.setObjectName("TimeBar")
        elapsedTimeBar.setRange(0, 100)
        elapsedTimeBar.setValue(time_percentage)
        elapsedTimeBar.setFixedHeight(15)
        elapsedTimeBar.setTextVisible(False)

        # Percentage labels
        percentageLabel = QLabel(f"{progress_value}%")
        percentageLabel.setFixedWidth(40)

        timePercentageLabel = QLabel(f"{time_percentage}%")
        timePercentageLabel.setFixedWidth(40)

        # Assemble widgets
        progress_stack_layout.addWidget(progressBar)
        progress_stack_layout.addWidget(elapsedTimeBar)
        progress_stack_frame.setLayout(progress_stack_layout)

        percentage_stack_layout.addWidget(percentageLabel)
        percentage_stack_layout.addWidget(timePercentageLabel)
        percentage_stack_frame.setLayout(percentage_stack_layout)

        # Add the project name, bars, and percentages
        project_layout.addWidget(project_label)
        project_layout.addWidget(progress_stack_frame, 1)
        project_layout.addWidget(percentage_stack_frame)
        project_frame.setLayout(project_layout)
        return project_frame

