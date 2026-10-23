from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal

from pages.base_page import BasePage
from pages.account.user import find_user

class SignInPage(BasePage):
    switch_to_Register = Signal()
    switch_to_ForgotPassword = Signal()
    login_success = Signal(object)

    def __init__(self):
        super().__init__()

    def define_layout(self) -> None:
        super().define_layout()
        self.layout.setSpacing(8)

        self.top_frame = QFrame()
        self.top_frame.setObjectName("TopBar")
        
        self.top_bar = QHBoxLayout()
        self.top_bar.addStretch()

        self.main_frame = QFrame()
        self.main_section = QVBoxLayout()

    def define_widgets(self) -> None:
        ## Header
        # Navigation
        self.nav_btn = QPushButton("Register")
        self.nav_btn.setObjectName("NavButton")
        self.nav_btn.setCursor(Qt.PointingHandCursor)
        self.nav_btn.clicked.connect(self.switch_to_Register.emit)

        # Theme toggle
        self.toggle_btn = QPushButton("🌑 Dark Mode")
        self.toggle_btn.setObjectName("ToggleButton")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)

        ## Main section
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
        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.hide()

        self.login_btn = QPushButton("Sign In")
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.attempt_login)
        self.password_input.returnPressed.connect(self.attempt_login)

        self.forgot_btn = QPushButton("Forgotten Password?")
        self.forgot_btn.setObjectName("NavButton")
        self.forgot_btn.setCursor(Qt.PointingHandCursor)
        self.forgot_btn.clicked.connect(self.switch_to_ForgotPassword.emit)

    def assemble_widgets(self) -> None:
        # Header
        self.top_bar.addWidget(self.nav_btn)
        self.top_bar.addWidget(self.toggle_btn)
        self.top_frame.setLayout(self.top_bar)

        # Main section
        self.main_section.addWidget(self.title)
        self.main_section.addWidget(self.heading)
        self.main_section.addSpacing(5)
        self.main_section.addWidget(self.subheading)
        self.main_section.addSpacing(10)
        self.main_section.addWidget(self.email_input)
        self.main_section.addWidget(self.password_input)
        self.main_section.addWidget(self.error_label)
        self.main_section.addSpacing(10)
        self.main_section.addWidget(self.login_btn)
        self.main_section.addSpacing(3)
        self.main_section.addWidget(self.forgot_btn)

        self.main_frame.setLayout(self.main_section)
        self.main_frame.setFixedWidth(500)

        # Layout
        self.layout.addWidget(self.top_frame)
        self.layout.addSpacing(10)
        self.layout.addStretch(1)
        self.layout.addWidget(self.main_frame, alignment=Qt.AlignHCenter)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def attempt_login(self) -> None:
        user = find_user(self.email_input.text(), self.password_input.text())

        if user is None:
            self.error_label.setText("Incorrect email or password.")
            self.error_label.show()
            return

        self.error_label.hide()
        self.email_input.clear()
        self.password_input.clear()
        self.login_success.emit(user)