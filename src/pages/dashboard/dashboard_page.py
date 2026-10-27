from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *#(QPushButton, QProgressBar, QLabel, 
                               #QWidget, QHBoxLayout, QVBoxLayout,
                               #QFrame)

from pages.base_page import BasePage

class DashboardPage(BasePage):
    switch_to_signin = Signal()
    switch_to_training = Signal()
    switch_to_account = Signal()
    switch_to_notifications = Signal()
    switch_to_employee = Signal()
    switch_to_manager = Signal()

    #Variables for testing - will be taken from to-do in future
    projectNum = 3
    projectName = "testing :)"
    progressValue = 23
    totalTime = 180
    timeTaken = 60
    timePercentage = int((timeTaken/totalTime) * 100)

    def __init__(self):
        self.current_user = None
        super().__init__()

        #need to create a widget to show estimated percentage of time completed
    
    def create_progress_bar(self, project_name, progress_value, time_percentage):

        # Create project label
        project_label = QLabel(project_name)
        project_label.setObjectName("projectLabel")
        project_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        project_label.setFixedWidth(100)

        # Create project completion progress bar
        progressBar = QProgressBar()
        progressBar.setRange(0, 100)
        progressBar.setValue(progress_value)
        progressBar.setFixedHeight(15)
        progressBar.setTextVisible(False)

        progressBar.setStyleSheet("QProgressBar {background-color: #D6D4D4;border-radius: 5px} QProgressBar::chunk {background-color: #EAB308; border-radius: 5px}")

        # Create time tracking progress bar
        elapsedTimeBar = QProgressBar()
        elapsedTimeBar.setObjectName("TimeBar")
        elapsedTimeBar.setRange(0, 100)
        elapsedTimeBar.setValue(time_percentage)
        elapsedTimeBar.setFixedHeight(15)
        elapsedTimeBar.setTextVisible(False)

        elapsedTimeBar.setStyleSheet("QProgressBar { background-color: #D6D4D4; border-radius: 5px} QProgressBar::chunk {background-color: #EAB308;border-radius: 5px}")

        # Create percentage labels
        percentageLabel = QLabel(f"{progress_value}%")
        timePercentageLabel = QLabel(f"{time_percentage}%")

        percentageLabel.setFixedWidth(40)
        timePercentageLabel.setFixedWidth(40)

        # Create a vertical layout for the two progress bars
        progress_stack = QWidget()
        progress_stack_layout = QVBoxLayout(progress_stack)

        progress_stack_layout.setContentsMargins(0, 0, 0, 0)
        progress_stack_layout.setSpacing(5)

        progress_stack_layout.addWidget(progressBar)
        progress_stack_layout.addWidget(elapsedTimeBar)

        # Create a vertical layout for the percentages
        percentage_stack = QWidget()
        percentage_stack_layout = QVBoxLayout(percentage_stack)

        percentage_stack_layout.setContentsMargins(0, 0, 0, 0)
        percentage_stack_layout.setSpacing(5)

        percentage_stack_layout.addWidget(percentageLabel)
        percentage_stack_layout.addWidget(timePercentageLabel)

        # Create the main project container
        project_container = QWidget()
        project_layout = QHBoxLayout(project_container)

        project_layout.setContentsMargins(10, 5, 10, 5)
        project_layout.setSpacing(10)

        # Add the project name, bars, and percentages
        project_layout.addWidget(project_label)
        project_layout.addWidget(progress_stack, 1)
        project_layout.addWidget(percentage_stack)

        return project_container

    

    def define_widgets(self) -> None:


        # Define the buttons for the dashboard page
        self.training = QPushButton("Training")
        self.account = QPushButton("Account")
        self.notifications = QPushButton("Notifs")
        self.view_employee_dashboard = QPushButton("Employee Dashboard")
        

        # define boxes for the dashboard page
        self.overdue_box = QGroupBox("Overdue Tasks")
        self.upcoming_box = QGroupBox("Upcoming Tasks")
        self.completed_box = QGroupBox("Completed Tasks")

        # Create layout of the boxes
        self.overdue_layout = QVBoxLayout()
        self.upcoming_layout = QVBoxLayout()
        self.completed_layout = QVBoxLayout()

        # Assign layouts to the boxes
        self.overdue_box.setLayout(self.overdue_layout)
        self.upcoming_box.setLayout(self.upcoming_layout)
        self.completed_box.setLayout(self.completed_layout)

        #Progress tracker layout
        self.prog_frame = QFrame()
        self.prog_frame.setObjectName("ProgressFrame")
        self.prog_frame.setFrameShape(QFrame.Shape.Box)
        self.prog_frame_layout = QVBoxLayout()
        self.prog_frame.setLayout(self.prog_frame_layout)

        #Default layout - no projects
        self.progressTrackerHeader = QLabel("Progress Tracker")
        self.progressTrackerHeader.setObjectName("ProgressTrackerHeader")
        self.progressTrackerHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressTrackerHeader.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.noProjectLabel = QLabel("No projects currently being tracked.")
        self.noProjectLabel.setObjectName("noProjectLabel")
        self.noProjectLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #progress bar widget layout
        self.progress_container = QWidget()
        self.progress_container.setContentsMargins(10, 10, 10, 10)

        progress_layout = QVBoxLayout(self.progress_container)
        progress_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add the frame to the progress container
        progress_layout.addWidget(self.prog_frame)

        # Add the heading once
        self.prog_frame_layout.addWidget(self.progressTrackerHeader)

        # Add projects
        if self.projectNum == 0:
            self.prog_frame_layout.addWidget(self.noProjectLabel)

        elif self.projectNum >= 1:
            for i in range(self.projectNum):
                self.prog_frame_layout.addWidget(
                    self.create_progress_bar(self.projectName, self.progressValue, self.timePercentage)
                )
        else:
            print("Error. Unexpected scenario in dashboard.py")

        self.todo = QPushButton("To-Do List")

        self.training.setCursor(Qt.PointingHandCursor)
        self.training.setObjectName("trainingButton")
        self.training.clicked.connect(self.switch_to_training.emit)
        self.account.setCursor(Qt.PointingHandCursor)
        self.account.setObjectName("accountButton")
        self.account.clicked.connect(self.switch_to_account.emit)
        self.notifications.setCursor(Qt.PointingHandCursor)
        self.notifications.setObjectName("notificationsButton")
        self.notifications.clicked.connect(self.switch_to_notifications.emit)
        self.view_employee_dashboard.setCursor(Qt.PointingHandCursor)
        self.view_employee_dashboard.setObjectName("employeeDashboardButton")
        self.view_employee_dashboard.clicked.connect(self.open_staff_dashboard)
        self.view_employee_dashboard.setVisible(False)  # Initially hidden, will be shown based on user rank


        self.widgets = (self.training, self.account, self.notifications, self.view_employee_dashboard)


    def set_current_user(self, user):
        self.current_user = user

        # Hide button if nobody is signed in
        if user is None:
            self.view_employee_dashboard.setVisible(False)
            return

        # Manager
        if user.rank == "Manager":
            self.view_employee_dashboard.setText("Manager Dashboard")
            self.view_employee_dashboard.setVisible(True)

        # Team Leader
        elif user.rank == "Team Lead":
            self.view_employee_dashboard.setText("Employee Dashboard")
            self.view_employee_dashboard.setVisible(True)

        # Regular Employee
        else:
            self.view_employee_dashboard.setVisible(False)

    def open_staff_dashboard(self):

        if self.current_user is None:
            return

        if self.current_user.rank == "Manager":
            self.switch_to_manager.emit()

        elif self.current_user.rank == "Team Lead":
            self.switch_to_employee.emit()
                
    def assemble_widgets(self) -> None:

        
        # Create the main layout for the dashboard page 
        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(20)

        # set layout for buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)

        # layout properties for buttons
        self.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        

        # set layout properties of boxes
        self.task_layout = QHBoxLayout()
        self.task_layout.setSpacing(10)

        self.task_layout.addWidget(self.overdue_box)
        self.task_layout.addWidget(self.upcoming_box)
        self.task_layout.addWidget(self.completed_box)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.progress_container)
        self.layout.addStretch()
        self.layout.addLayout(self.task_layout)
        self.setLayout(self.layout)

        # set the style for the boxes
        for box in (self.overdue_box, self.upcoming_box, self.completed_box):

            box.setFixedHeight(200)

            box.setStyleSheet(" QGroupBox {border: 4px solid #EAB308;border-radius: 8px; margin-top:15px; padding: 10px;font-size: 14px; font-weight: bold} QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px;}")

        # Set the style for the buttons
        self.training.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.account.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.notifications.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.view_employee_dashboard.setStyleSheet("background-color: #EAB308; font-weight: bold")
        
        for widget in self.widgets:
            self.button_layout.addWidget(widget)
            
            

        self.setLayout(self.layout)
