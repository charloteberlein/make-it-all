from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from pages.base_page import BasePage

class DashboardPage(BasePage):
    switch_to_signin= Signal()
    switch_to_training = Signal()
    switch_to_account = Signal()
    switch_to_notifications = Signal()
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:


        # Define the buttons for the dashboard page
        self.posts = QPushButton("Posts")
        self.todo = QPushButton("To-do")
        self.training = QPushButton("Training")
        self.account = QPushButton("Account")
        self.notifications = QPushButton("Notifs")
        self.back_btn = QPushButton("LogOut")

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

        self.training.setCursor(Qt.PointingHandCursor)
        self.training.setObjectName("trainingButton")
        self.training.clicked.connect(self.switch_to_training.emit)
        self.account.setCursor(Qt.PointingHandCursor)
        self.account.setObjectName("accountButton")
        self.account.clicked.connect(self.switch_to_account.emit)
        self.notifications.setCursor(Qt.PointingHandCursor)
        self.notifications.setObjectName("notificationsButton")
        self.notifications.clicked.connect(self.switch_to_notifications.emit)
        
        
        self.widgets = (self.training, self.account, self.notifications)

        
        
        
    def assemble_widgets(self) -> None:

        
        # Create the main layout for the dashboard page 
        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(20)

        # set layout for buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)

        # layout properties for buttons
        self.setFont(self.posts.font())
        self.setFont(QFont("Arial", 4))
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # set layout properties of boxes
        self.task_layout = QHBoxLayout()
        self.task_layout.setSpacing(10)

        self.task_layout.addWidget(self.overdue_box)
        self.task_layout.addWidget(self.upcoming_box)
        self.task_layout.addWidget(self.completed_box)
        self.layout.addLayout(self.button_layout)
        self.layout.addStretch()
        self.layout.addLayout(self.task_layout)
        self.setLayout(self.layout)

        # set the style for the boxes
        for box in (self.overdue_box, self.upcoming_box, self.completed_box):

            box.setFixedHeight(300)

            box.setStyleSheet("""
                QGroupBox {
                    border: 4px solid #EAB308;
                    border-radius: 8px;
                    margin-top:15px;
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                }

                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
            """)

        # Set the style for the buttons
        self.training.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.account.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.notifications.setStyleSheet("background-color: #EAB308; font-weight: bold")
        
        for widget in self.widgets:
            self.button_layout.addWidget(widget)

        self.setLayout(self.layout)
