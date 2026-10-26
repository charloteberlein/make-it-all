from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QPushButton, QProgressBar, QLabel, 
    QWidget, QHBoxLayout, QVBoxLayout,
    QFrame, QScrollArea)

from pages.base_page import BasePage
from pages.projects.projects import Project

class DashboardPage(BasePage):

    # project attributes
    # project_id : int, name: str, progress: int, total_time: int, time_taken: int
    projectList = [Project(1, "Project 1: Team Project",56, 120, 54)]

    # switch_to_signin= Signal()
    # switch_to_training = Signal()
    # switch_to_account = Signal()
    # switch_to_notifications = Signal()
    # switch_to_employee = Signal()
    # switch_to_manager = Signal()

    def __init__(self):
        super().__init__()



    def createProgressBar(self, projectName, progressValue, timePercentage):
        #creating a project label
        project_label = QLabel(projectName)
        project_label.setObjectName("projectLabel")
        project_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        #creating a progressbar
        progressBar = QProgressBar()
        progressBar.setObjectName("ProjectProgress")
        progressBar.setRange(0,100)
        progressBar.setValue(progressValue) 

        progress_bar_label = QLabel("Project progress:")
        progress_bar_label.setObjectName("ProgressBarLabel")


        # Creating time tracking progress bar
        elapsedTimeBar = QProgressBar()
        elapsedTimeBar.setObjectName("TimeBar")
        elapsedTimeBar.setRange(0,100)
        elapsedTimeBar.setValue(int(timePercentage))

        time_bar_label = QLabel("Time elapsed:")
        time_bar_label.setObjectName("ProgressBarLabel")

        #Progress bar layouts:
        prog_bar_widget = QWidget()
        prog_bar_layout = QVBoxLayout(prog_bar_widget)
        prog_bar_layout.addWidget(progress_bar_label)
        prog_bar_layout.addWidget(progressBar)

        time_bar_widget = QWidget()
        time_bar_layout = QVBoxLayout(time_bar_widget)
        time_bar_layout.addWidget(time_bar_label)
        time_bar_layout.addWidget(elapsedTimeBar)

        progress_stack = QWidget()
        progress_stack_layout = QVBoxLayout(progress_stack)
        progress_stack_layout.addWidget(prog_bar_widget)
        progress_stack_layout.addWidget(time_bar_widget)

        project_container = QWidget()
        project_layout = QHBoxLayout(project_container)

        project_layout.addWidget(project_label)
        project_layout.addWidget(progress_stack)

        return project_container

    def define_layout(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(35, 30, 35, 30)
        self.layout.setSpacing(14)

        # Dashboard scrollbar widget
        self.dashboard_content = QWidget()
        self.dashboard_content_layout = QVBoxLayout(self.dashboard_content)

        # temp horizontal navigation bar - should be replaced by EC code later
        self.navbar_container = QWidget()
        self.navbar_layout = QHBoxLayout(self.navbar_container)
        #navbar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Progress bar widget layout
        self.progress_container = QWidget()
        self.progress_layout = QVBoxLayout(self.progress_container)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_area.setWidget(self.dashboard_content)
        self.dashboard_content_layout.addWidget(self.navbar_container)
        self.dashboard_content_layout.addWidget(self.progress_container)




    def define_widgets(self) -> None:
        # Navbar buttons - TEMPORARY 
        self.posts = QPushButton("View posts")
        self.todo = QPushButton("View To-do")
        self.projects = QPushButton("View Projects")
        self.account = QPushButton("Account")

        # Apply the same cursor to every button
        for button in (
            self.posts, self.todo,
            self.projects, self.account):
            button.setCursor(Qt.CursorShape.PointingHandCursor)


        #Progress tracker layout
        self.prog_frame = QFrame()
        self.prog_frame.setObjectName("ProgressFrame")
        self.prog_frame.setFrameShape(QFrame.Shape.Box)

        self.prog_frame_layout = QVBoxLayout()
        self.prog_frame.setLayout(self.prog_frame_layout)
    
        self.progressTrackerHeader = QLabel("Progress Tracker")
        self.progressTrackerHeader.setObjectName("ProgressTrackerHeader")
        self.progressTrackerHeader.setAlignment(Qt.AlignmentFlag.AlignTop)

        #Default layout - no projects
        self.noProjectLabel = QLabel("No projects currently being tracked.")
        self.noProjectLabel.setObjectName("noProjectLabel")
        self.noProjectLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.navbar_layout.addWidget(self.posts)
        self.navbar_layout.addWidget(self.todo)
        self.navbar_layout.addWidget(self.projects)
        self.navbar_layout.addWidget(self.account)


        #progress_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.progress_layout.addWidget(self.progressTrackerHeader)
        self.progress_layout.addSpacing(5)
        self.progress_layout.addWidget(self.prog_frame)

        if (len(self.projectList) < 0):
            self.prog_frame_layout.addWidget(self.noProjectLabel)

        for project in self.projectList:
            self.prog_frame_layout.addWidget(
                self.createProgressBar(
                    project.name,
                    project.progress,
                    project.timePercentage
                )
            )

        
        # Assemble widgets
        self.widgets = (
            self.scroll_area, 
        )

