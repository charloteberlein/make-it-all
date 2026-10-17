import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QStackedWidget
)
# from PySide6.QtCore import Qt
from pages.signin import SignInPage
from pages.register import RegisterPage
from pages.posts import TopicsPage
from pages.dashboard import DashboardPage
from pages.todo import TodoPage
from pages.forgotpassword import ForgotPasswordPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Make-It-All Demo")
        self.setFixedSize(380, 420)

        self.is_dark_mode = False

        # Container
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Pages
        self.stacked_widget = QStackedWidget()

        self.signin_page = SignInPage()
        self.register_page = RegisterPage()
        self.topics_page = TopicsPage()
        self.dashboard_page = DashboardPage()
        self.todo_page = TodoPage()
        self.forgot_password_page = ForgotPasswordPage()

        self.stacked_widget.addWidget(self.signin_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.topics_page)
        self.stacked_widget.addWidget(self.todo_page)
        self.stacked_widget.addWidget(self.forgot_password_page)

        main_layout.addWidget(self.stacked_widget)

        # Navigation events
        self.signin_page.switch_to_Register.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.register_page.switch_to_SignIn.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.signin_page.switch_to_ForgotPassword.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.forgot_password_page.switch_to_SignIn.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        # Colour theme events
        self.signin_page.toggle_btn.clicked.connect(self.toggle_theme)
        self.register_page.toggle_btn.clicked.connect(self.toggle_theme)
        self.forgot_password_page.toggle_btn.clicked.connect(self.toggle_theme)

        # Page events
        self.signin_page.login_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.register_page.login_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.forgot_password_page.login_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.dashboard_page.posts.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.dashboard_page.todo.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        self.apply_theme()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        theme_text = "☀️ Light Mode" if self.is_dark_mode else "🌑 Dark Mode"

        self.signin_page.toggle_btn.setText(theme_text)
        self.register_page.toggle_btn.setText(theme_text)

        self.apply_theme()

    def apply_theme(self):
        filename = "dark.qss" if self.is_dark_mode else "light.qss"
        filepath = f"styles/{filename}"
        with open(filepath, "r") as file:
            self.setStyleSheet(file.read())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())