from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel
)
from PySide6.QtCore import Qt, Signal

class SignInPage(QWidget):
    switch_to_Register = Signal()

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.init_ui()

    def init_ui(self):
        # Set up container, and its size.
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(35, 30, 35, 30)
        self.layout.setSpacing(14)

        # Top Bar with Colour Theme Toggle
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        self.nav_btn = QPushButton("Register")
        self.nav_btn.setObjectName("NavButton")
        self.nav_btn.setCursor(Qt.PointingHandCursor)
        self.nav_btn.clicked.connect(self.switch_to_Register.emit)
        top_bar.addWidget(self.nav_btn)

        # Theme Toggle Button
        self.toggle_btn = QPushButton("🌑 Dark Mode")
        self.toggle_btn.setObjectName("ToggleButton")
        self.toggle_btn.setCursor(Qt.PointingHandCursor) # Lets user know item is interactable.
        top_bar.addWidget(self.toggle_btn)
        self.layout.setSpacing(8)

        # Header Section, Object names used to reference assets in stylesheet.
        self.title = QLabel("Make-It-All")
        self.title.setObjectName("TitleLabel")
        
        self.heading = QLabel("Sign In")
        self.heading.setObjectName("HeadingLabel")
        
        self.subheading = QLabel("Enter your company credentials to continue.")
        self.subheading.setObjectName("SubheadingLabel")

        # Input Fields for Company Email and Password
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter company email (xxx@make-it-all.co.uk)")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Main Sign In button - generic LoginButton asset used for both Sign in and Register page.
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.setCursor(Qt.PointingHandCursor)

        # Assembles UI Layout with previous assets.
        self.layout.addLayout(top_bar)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.subheading)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_input)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.login_btn)
        self.layout.addStretch()

        self.setLayout(self.layout)


