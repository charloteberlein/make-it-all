from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal

from pages.base_page import BasePage

class SignInPage(BasePage):
    switch_to_Register = Signal()

    def __init__(self):
        super().__init__()

    def define_layout(self) -> None:
        super().define_layout()
        self.layout.setSpacing(8)

    def define_widgets(self) -> None:
        # Navigation
        self.top_bar = QHBoxLayout()
        self.top_bar.addStretch()

        self.nav_btn = QPushButton("Register")
        self.nav_btn.setObjectName("NavButton")
        self.nav_btn.setCursor(Qt.PointingHandCursor)
        self.nav_btn.clicked.connect(self.switch_to_Register.emit)
        self.top_bar.addWidget(self.nav_btn)

        # Theme toggle
        self.toggle_btn = QPushButton("🌑 Dark Mode")
        self.toggle_btn.setObjectName("ToggleButton")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.top_bar.addWidget(self.toggle_btn)

        # Header (references stylesheet)
        self.title = QLabel("Make-It-All")
        self.title.setObjectName("TitleLabel")
        
        self.heading = QLabel("Sign In")
        self.heading.setObjectName("HeadingLabel")
        
        self.subheading = QLabel("Enter your company credentials to continue.")
        self.subheading.setObjectName("SubheadingLabel")

        # Login
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter company email (xxx@make-it-all.co.uk)")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Sign In")
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.setCursor(Qt.PointingHandCursor)

    def assemble_widgets(self) -> None:
        self.layout.addLayout(self.top_bar)
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


