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
        

        self.posts.setCursor(Qt.PointingHandCursor)
        self.todo.setCursor(Qt.PointingHandCursor)
        self.training.setCursor(Qt.PointingHandCursor)
        self.training.setObjectName("trainingButton")
        self.training.clicked.connect(self.training.emit)
        self.account.setCursor(Qt.PointingHandCursor)
        self.account.setObjectName("accountButton")
        self.account.clicked.connect(self.account.emit)
        self.notifications.setCursor(Qt.PointingHandCursor)
        self.notifications.setObjectName("notificationsButton")
        self.notifications.clicked.connect(self.notifications.emit)
        self.back_btn.setObjectName("logoutButton")
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.clicked.connect(self.switch_to_signin.emit)
        
        self.widgets = (self.posts, self.todo, self.training, self.account, self.notifications, self.back_btn)

        
        
        
    def assemble_widgets(self) -> None:
        self.layout = QHBoxLayout()

        # Set the layout properties
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(5)
        self.setFont(self.posts.font())
        self.setFont(QFont("Arial", 4))
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Set the style for the buttons
        self.posts.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.todo.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.training.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.account.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.notifications.setStyleSheet("background-color: #EAB308; font-weight: bold")
        self.back_btn.setStyleSheet("background-color: #EAB308; font-weight: bold")

        for widget in self.widgets:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)
