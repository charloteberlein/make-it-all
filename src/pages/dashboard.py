from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QPushButton, QProgressBar, QLabel, 
                               QWidget, QHBoxLayout, QVBoxLayout,
                               QFrame)
from PySide6 import QtQuick

from pages.base_page import BasePage

class DashboardPage(BasePage):
    projectNo = 0
    # Constructor
    def __init__(self):
        super().__init__()

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

        #Progress bar widgets
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0,100)
        self.progressBar.setValue(24) # value will need data from to-do pages
        self.progressBar.setMinimumHeight(20)

        self.prog_frame = QFrame()
        self.prog_frame.setObjectName("ProgressFrame")
        self.prog_frame.setFrameShape(QFrame.Shape.Box)
        self.prog_frame_layout = QVBoxLayout()
        self.prog_frame.setLayout(self.prog_frame_layout)

        self.noProjectLabel = QLabel("No projects currently being tracked.")
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

        # self.progress_container.setMinimumHeight(60)
        # self.progress_container.setMinimumWidth(200)
        progress_layout = QVBoxLayout(self.progress_container)
        progress_layout.setAlignment(Qt.AlignmentFlag.AlignTop)


        progress_layout.addWidget(self.prog_frame)
        # progress_layout.addWidget(self.progressBar)

        self.prog_frame_layout.addWidget(self.noProjectLabel)
        self.prog_frame_layout.addWidget(self.progressBar)

        #Determine number of progress bars needed. 
        def progBarNumber():
            pass


        # Assemble widgets
        self.widgets = (
            self.navbar_container,
            self.progress_container
        )
