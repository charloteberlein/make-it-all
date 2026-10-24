from PySide6.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, Signal

from pages.base_page import BasePage
from pages.account.user import *

class RegisterPage(BasePage):
    switch_to_SignIn = Signal()
    login_success = Signal(object)

    def __init__(self):
        super().__init__()

    def define_layout(self):
        super().define_layout()
        self.layout.setSpacing(8)

        self.top_frame = QFrame()
        self.top_frame.setObjectName("TopBar")

        self.top_bar = QHBoxLayout()
        self.top_bar.addStretch()

        self.main_frame = QFrame()
        self.main_section = QVBoxLayout()
        self.name_layout = QHBoxLayout()
        self.name_layout.setSpacing(10)

    def define_widgets(self) -> None:
        ## Header
        # Navigation
        self.nav_btn = QPushButton("Sign In")
        self.nav_btn.setObjectName("NavButton")
        self.nav_btn.setCursor(Qt.PointingHandCursor)
        self.nav_btn.clicked.connect(self.switch_to_SignIn.emit)

        # Theme toggle
        self.toggle_btn = QPushButton("🌑 Dark Mode")
        self.toggle_btn.setObjectName("ToggleButton")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)

        ## Main section
        # Header (references stylesheet)
        self.title = QLabel("Make-It-All")
        self.title.setObjectName("TitleLabel")
        
        self.heading = QLabel("Register")
        self.heading.setObjectName("HeadingLabel")
        
        self.subheading = QLabel("Set up your company credentials to get started.")
        self.subheading.setObjectName("SubheadingLabel")

        # Login
        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("Enter Firstname")
        self.lastname_input = QLineEdit()
        self.lastname_input.setPlaceholderText("Enter Lastname")
        self.name_layout.addWidget(self.firstname_input)
        self.name_layout.addWidget(self.lastname_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter company email (xxx@make-it-all.co.uk)")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Register")
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.create_account)

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
        self.main_section.addLayout(self.name_layout)
        self.main_section.addWidget(self.email_input)
        self.main_section.addWidget(self.password_input)
        self.main_section.addWidget(self.confirm_password_input)
        self.main_section.addSpacing(10)
        self.main_section.addWidget(self.login_btn)

        self.main_frame.setLayout(self.main_section)
        self.main_frame.setFixedWidth(500)

        # Layout
        self.layout.addWidget(self.top_frame)
        self.layout.addSpacing(10)
        self.layout.addStretch(1)
        self.layout.addWidget(self.main_frame, alignment=Qt.AlignHCenter)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def create_account(self) -> None:
        email = self.email_input.text().strip().lower()
        firstname = self.firstname_input.text()
        lastname = self.lastname_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        error_message = validate_registration_inputs(email, firstname, lastname, password, confirm_password)
        if error_message:
            self.show_message(error_message)
            return

        success = create_user_account(email, firstname, lastname, password)
        if success:
            user = find_user(email, password)
            if user:
                self.subheading.setText("")
                self.firstname_input.clear()
                self.lastname_input.clear()
                self.email_input.clear()
                self.password_input.clear()
                self.confirm_password_input.clear()
                self.login_success.emit(user)
            else:
                self.show_message("❌ Error logging in after account creation.")
        else:
            self.show_message("❌ This user account is already registered. Please Sign In.")

    def show_message(self, message: str) -> None:
        """ Updates the subheading text directly to show errors or success. """
        self.subheading.setStyleSheet("color: #e74c3c; font-size: 14px;")
        self.subheading.setText("")
        self.subheading.setText(message)