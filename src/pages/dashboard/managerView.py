from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *#(QPushButton, QProgressBar, QLabel, 
                                #QWidget, QHBoxLayout, QVBoxLayout,
                                #QFrame)
from PySide6 import QtQuick

from pages.base_page import BasePage

class ManagerPage(BasePage):

    switch_to_dashboard = Signal()
    
    def __init__(self):
        self.current_user = None
        super().__init__()

    

    def define_widgets(self) -> None:


        # Define the buttons for each project
        self.project1 = QPushButton("Project 1")
        self.project2 = QPushButton("Project 2")
        self.project3 = QPushButton("Project 3")
        self.back = QPushButton("Back to Dashboard")
        

        self.project1.setCursor(Qt.PointingHandCursor)
        self.project1.setObjectName("project1Button")
        self.project2.setCursor(Qt.PointingHandCursor)
        self.project2.setObjectName("project2Button")
        self.project3.setCursor(Qt.PointingHandCursor)
        self.project3.setObjectName("project3Button")
        self.back.setCursor(Qt.PointingHandCursor)
        self.back.setObjectName("backButton")   
        self.back.clicked.connect(self.switch_to_dashboard.emit)
        

        self.widgets = (self.project1, self.project2, self.project3, self.back)

                
    def assemble_widgets(self) -> None:

        # Create the main vertical layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(20)

        # Create horizontal layout for project buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)

        # Set font
        self.setFont(QFont("Arial", 9, QFont.Weight.Bold))

        # Style the buttons
        self.project1.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.project2.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.project3.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.back.setStyleSheet("background-color: #EAB308; font-weight: bold")

        # Add buttons to horizontal layout
        for widget in self.widgets:
            self.button_layout.addWidget(widget)

        # Add horizontal button layout to main vertical layout
        self.layout.addLayout(self.button_layout)

        # Push buttons to the top of the page
        self.layout.addStretch()

        # Set the main layout
        self.setLayout(self.layout)