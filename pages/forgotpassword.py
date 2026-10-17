from PySide6.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal

from pages.base_page import BasePage

class ForgotPasswordPage(BasePage):
    switch_to_SignIn = Signal()

    def __init__(self):
        super().__init__()

    def define_layout(self) -> None:
        super().define_layout()
        self.layout.setSpacing(8)

    def define_widgets(self) -> None:
        # Navigation
        self.top_frame = QFrame()
        self.top_frame.setObjectName("TopBar")

        self.top_bar = QHBoxLayout()
        self.top_bar.addStretch()

        self.nav_btn = QPushButton("Sign In")
        self.nav_btn.setObjectName("NavButton")
        self.nav_btn.setCursor(Qt.PointingHandCursor)
        self.nav_btn.clicked.connect(self.switch_to_SignIn.emit)
        self.top_bar.addWidget(self.nav_btn)

        # Theme toggle
        self.toggle_btn = QPushButton("🌑 Dark Mode")
        self.toggle_btn.setObjectName("ToggleButton")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.top_bar.addWidget(self.toggle_btn)

        self.top_frame.setLayout(self.top_bar)

        # Header (references stylesheet)
        self.title = QLabel("Make-It-All")
        self.title.setObjectName("TitleLabel")
        
        self.heading = QLabel("Forgot Password?")
        self.heading.setObjectName("HeadingLabel")
        
        self.subheading = QLabel("Enter your new password to continue.")
        self.subheading.setObjectName("SubheadingLabel")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your new password.")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Re-enter your new password.")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Reset Password && Sign In")
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.setCursor(Qt.PointingHandCursor)

    def assemble_widgets(self) -> None:
        self.layout.addWidget(self.top_frame)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.subheading)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.confirm_password_input)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.login_btn)
        self.layout.addStretch()

        self.setLayout(self.layout)