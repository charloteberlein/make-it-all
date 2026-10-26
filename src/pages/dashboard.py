from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QPushButton, QProgressBar, QLabel, 
    QWidget, QHBoxLayout, QVBoxLayout,
    QFrame, QScrollArea)

from pages.base_page import BasePage

class DashboardPage(BasePage):
    projectNum = 3
    projectName = "testing :)"
    progressValue = 23
    totalTime = 180
    timeTaken = 60
    timePercentage = (timeTaken/totalTime) * 100

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

        # Creating time tracking progress bar
        elapsedTimeBar = QProgressBar()
        elapsedTimeBar.setObjectName("TimeBar")
        elapsedTimeBar.setRange(0,100)
        elapsedTimeBar.setValue(int(timePercentage))

        #Progress bar layouts
        progress_stack = QWidget()
        progress_stack_layout = QVBoxLayout(progress_stack)
        progress_stack_layout.addWidget(progressBar)
        progress_stack_layout.addWidget(elapsedTimeBar)

        project_container = QWidget()
        project_layout = QHBoxLayout(project_container)

        project_layout.addWidget(project_label)
        project_layout.addWidget(progress_stack)

        return project_container
 
              
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

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
    
        self.progressTrackerHeader = QLabel("Progress Tracker")
        self.progressTrackerHeader.setObjectName("ProgressTrackerHeader")
        self.progressTrackerHeader.setAlignment(Qt.AlignmentFlag.AlignTop)

        #Default layout - no projects
        self.noProjectLabel = QLabel("No projects currently being tracked.")
        self.noProjectLabel.setObjectName("noProjectLabel")
        self.noProjectLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Dashboard scrollbar widget
        self.dashboard_content = QWidget()
        dashboard_content_layout = QVBoxLayout(self.dashboard_content)


        # temp horizontal navigation bar - should be replaced by EC code later
        self.navbar_container = QWidget()

        navbar_layout = QHBoxLayout(self.navbar_container)
        #navbar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        #navbar_layout.setContentsMargins(0, 0, 0, 0)
        navbar_layout.addWidget(self.posts)
        navbar_layout.addWidget(self.todo)
        navbar_layout.addWidget(self.projects)
        navbar_layout.addWidget(self.account)

        # Progress bar widget layout
        self.progress_container = QWidget()

        progress_layout = QVBoxLayout(self.progress_container)
        #progress_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        progress_layout.addWidget(self.progressTrackerHeader)
        progress_layout.addSpacing(10)
        progress_layout.addWidget(self.prog_frame)

        if (self.projectNum == 0):
            self.prog_frame_layout.addWidget(self.noProjectLabel)
        elif (self.projectNum >= 1):
            for i in range (self.projectNum):
                self.prog_frame_layout.addWidget(
                     self.createProgressBar(self.projectName, 
                        self.progressValue, self.timePercentage))
        else:
             print("Error. Unexpected scenario in dashboard.py")

        scroll_area.setWidget(self.dashboard_content)
        dashboard_content_layout.addWidget(self.navbar_container)
        dashboard_content_layout.addWidget(self.progress_container)
        
        # Assemble widgets
        self.widgets = (
            scroll_area, 
        )

