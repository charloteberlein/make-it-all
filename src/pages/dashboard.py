from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QPushButton, QProgressBar, QLabel, 
                               QWidget, QHBoxLayout, QVBoxLayout,
                               QFrame)
from PySide6 import QtQuick

from pages.base_page import BasePage

class DashboardPage(BasePage):
    projectNum = 3
    projectName = "testing :)"
    progressValue = 23
    totalTime = 180
    timeTaken = 60
    timePercentage = totalTime/timeTaken

    # Constructor
    def __init__(self):
        super().__init__()

# Need to create a widget to show percentage of estimated time completed

    # Function to create progress bar for each project.
    def createProgressBar(self, projectName, progressValue):
        #creating a project label
        project_label = QLabel(projectName)
        project_label.setObjectName("projectLabel")
        project_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        project_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        #creating a progressbar
        progressBar = QProgressBar()
        progressBar.setObjectName("ProjectProgress")
        progressBar.setRange(0,100)
        progressBar.setValue(progressValue) 
        progressBar.setMinimumHeight(20) 

        # Creating time tracking progress bar
        elapsedTimeBar = QProgressBar()
        elapsedTimeBar.setObjectName("TimeBar")
        elapsedTimeBar.setRange(0,100)
        elapsedTimeBar.setValue(self.timePercentage)
        elapsedTimeBar.setMinimumHeight(20) 

        #Progress bar layouts
        progress_stack = QWidget()
        progress_stack_layout = QVBoxLayout(progress_stack)
        progress_stack_layout.addWidget(progressBar)
        progress_stack_layout.addWidget(elapsedTimeBar)

        project_container = QWidget()
        #project_container.setContentsMargins(10, 10, 10, 10)
        project_layout = QHBoxLayout(project_container)
        project_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        project_layout.addWidget(project_label)
        project_layout.addWidget(progress_stack)

        return project_container
 
              
    def define_widgets(self) -> None:
        # Navbar buttons
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

        #Default layout - no projects
        self.progressTrackerHeader = QLabel("Progress Tracker")
        self.progressTrackerHeader.setObjectName("ProgressTrackerHeader")
        self.progressTrackerHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressTrackerHeader.setAlignment(Qt.AlignmentFlag.AlignTop)


        self.noProjectLabel = QLabel("No projects currently being tracked.")
        self.noProjectLabel.setObjectName("noProjectLabel")
        self.noProjectLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # temp horizontal navigation bar - should be replaced by EC code later
        self.navbar_container = QWidget()

        navbar_layout = QHBoxLayout(self.navbar_container)
        navbar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        navbar_layout.setContentsMargins(0, 0, 0, 0)
        navbar_layout.addWidget(self.posts)
        navbar_layout.addWidget(self.todo)
        navbar_layout.addWidget(self.projects)
        navbar_layout.addWidget(self.account)

        # Progress bar widget layout
        self.progress_container = QWidget()
        self.progress_container.setContentsMargins(10, 10, 10, 10)

        progress_layout = QVBoxLayout(self.progress_container)
        progress_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        progress_layout.addWidget(self.prog_frame)
        progress_layout.addWidget(self.progressTrackerHeader)
        progress_layout.addSpacing(10)

        if (self.projectNum == 0):
            self.prog_frame_layout.addWidget(self.progressTrackerHeader)
            self.prog_frame_layout.addWidget(self.noProjectLabel)
        elif (self.projectNum >= 1):
            for i in range (self.projectNum):
                self.prog_frame_layout.addWidget(self.progressTrackerHeader)
                self.prog_frame_layout.addWidget(
                     self.createProgressBar(self.projectName, 
                        self.progressValue))
        else:
             print("Error. Unexpected scenario in dashboard.py")

        # Assemble widgets
        # There's a big gap between navbar and progress widget that I don't know how to fix.
        self.widgets = (
            self.navbar_container,
            self.progress_container
        )

        #Determine number of progress bars needed. 
    def progBarNumber():
            #Take information from To-Do pages to determine number of projects. getter method?
            pass

        #Displays correct amount of progress bars. 
    def displayProgressBars():
            pass

        #function to determine layout
    # def progLayout(projectNum):
    #     if projectNum >= 1:
    #         for i in range (projectNum):
    #              createProgressBar()

