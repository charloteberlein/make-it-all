from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout

from pages.base_page import BasePage
from pages.account.user import User

class DashboardView(BasePage):
    switch_to_dashboard = Signal()
    
    def __init__(self):
        self.current_user: User | None = None
        super().__init__()

    def showEvent(self, event):
        # Grabs current user from Main Window on page load.
        super().showEvent(event)
        main_window = self.window()
        if hasattr(main_window, "current_user"):
            self.current_user = main_window.current_user

    def define_widgets(self) -> None:
        # Define the buttons for each project
        self.project1 = QPushButton("Project 1")
        self.project1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.project1.setObjectName("project1Button")

        self.project2 = QPushButton("Project 2")
        self.project2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.project2.setObjectName("project2Button")

        self.project3 = QPushButton("Project 3")
        self.project3.setCursor(Qt.CursorShape.PointingHandCursor)
        self.project3.setObjectName("project3Button")

        if self.current_user is not None and self.current_user.rank != "Manager":
            self.project3.hide()

        self.back = QPushButton("Back to Dashboard")
        self.back.clicked.connect(self.switch_to_dashboard.emit)
        self.back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back.setObjectName("backButton")

        self.widgets = (self.project1, self.project2, self.project3, self.back)
                
    def assemble_widgets(self) -> None:
        # Main vertical layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(20)

        # Project button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)

        # Add buttons to horizontal layout
        for widget in self.widgets:
            self.button_layout.addWidget(widget)

        self.layout.addLayout(self.button_layout)
        self.layout.addStretch()

        self.setLayout(self.layout)