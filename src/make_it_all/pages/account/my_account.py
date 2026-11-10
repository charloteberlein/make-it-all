from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from make_it_all.pages.base_page import BasePage


class MyAccountPage(BasePage):
    switch_to_ForgotPassword = Signal()
    switch_to_Dashboard = Signal()

    def __init__(self):
        super().__init__()

    def define_layout(self) -> None:
        super().define_layout()
        self.layout.setSpacing(8)

        self.top_bar = QHBoxLayout()
        self.top_bar.addStretch()

        self.main_frame = QFrame()
        self.main_section = QVBoxLayout()

    def define_widgets(self) -> None:
        self.heading = QLabel("Your Account")
        self.heading.setObjectName("HeadingLabel")

        self.subheading = QLabel("Your profile details and credentials.")
        self.subheading.setObjectName("SubheadingLabel")

        # Read-only input fields
        self.firstname_input = QLineEdit()
        self.firstname_input.setText("John")
        self.firstname_input.setReadOnly(True)

        self.lastname_input = QLineEdit()
        self.lastname_input.setText("Doe")
        self.lastname_input.setReadOnly(True)

        # Write-to input field
        self.preferred_name_input = QLineEdit()
        self.preferred_name_input.setText("Johnny")
        self.preferred_name_input.setPlaceholderText("Enter preferred name")

        self.change_btn = QPushButton("Save")
        self.change_btn.setObjectName("LoginButton")
        self.change_btn.setCursor(Qt.PointingHandCursor)
        self.change_btn.clicked.connect(self.switch_to_Dashboard.emit)

        self.email_input = QLineEdit()
        self.email_input.setText("john.doe@make-it-all.co.uk")
        self.email_input.setReadOnly(True)

        self.password_input = QLineEdit()
        self.password_input.setText("supersecret123")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setReadOnly(True)

        self.forgot_btn = QPushButton("Change/Forgot Password?")
        self.forgot_btn.setObjectName("NavButton")
        self.forgot_btn.setCursor(Qt.PointingHandCursor)
        self.forgot_btn.clicked.connect(self.switch_to_ForgotPassword.emit)

        self.nickname_layout = QHBoxLayout()
        self.nickname_layout.setContentsMargins(0, 0, 0, 0)
        self.nickname_layout.setSpacing(6)
        self.nickname_layout.addWidget(self.preferred_name_input)
        self.nickname_layout.addWidget(self.change_btn)

        self.form_layout = QFormLayout()
        self.form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.form_layout.setSpacing(10)
        self.form_layout.addRow("First Name:", self.firstname_input)
        self.form_layout.addRow("Last Name:", self.lastname_input)
        self.form_layout.addRow("Preferred Name:", self.nickname_layout)
        self.form_layout.addRow("Email:", self.email_input)
        self.form_layout.addRow("Password:", self.password_input)

    def assemble_widgets(self) -> None:
        self.main_section.addWidget(self.heading)
        self.main_section.addSpacing(5)
        self.main_section.addWidget(self.subheading)
        self.main_section.addSpacing(15)
        self.main_section.addLayout(self.form_layout)
        self.main_section.addSpacing(5)
        self.main_section.addWidget(self.forgot_btn)
        self.main_section.addStretch(1)

        self.main_frame.setLayout(self.main_section)
        self.main_frame.setFixedWidth(540)

        self.layout.addSpacing(10)
        self.layout.addWidget(self.main_frame, alignment=Qt.AlignHCenter)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def set_user(self, user) -> None:
        first_name, _, last_name = user.name.partition(" ")
        self.firstname_input.setText(first_name)
        self.lastname_input.setText(last_name)
        self.preferred_name_input.setText("")
        self.email_input.setText(user.email)
        self.password_input.setText(user.password)
