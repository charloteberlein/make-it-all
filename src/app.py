import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout, QFrame
)

# from PySide6.QtCore import Qt
from pages.page_index import PageIndex
from pages.header import Header
from pages.sidebar import Sidebar
from pages.signin import SignInPage
from pages.register import RegisterPage
from pages.posts import PostsPage
from pages.post import PostContentPage
from pages.dashboard import DashboardPage
from pages.todo import TodoPage
from pages.forgotpassword import ForgotPasswordPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Make-It-All Prototype")
        self.setFixedSize(1200, 800)

        self.is_dark_mode = False

        # Containers
        header_layout = QVBoxLayout(self)
        header_layout.setContentsMargins(0, 0, 0, 0)

        main_frame = QFrame()
        main_layout = QHBoxLayout()

        # Header & Sidebar
        self.header = Header()
        self.sidebar = Sidebar()

        # Pages
        self.stacked_widget = QStackedWidget()

        self.signin_page = SignInPage()
        self.register_page = RegisterPage()
        self.posts_page = PostsPage()
        self.post_page = PostContentPage()
        self.dashboard_page = DashboardPage()
        self.todo_page = TodoPage()
        self.forgot_password_page = ForgotPasswordPage()

        self.stacked_widget.addWidget(self.signin_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.todo_page)
        self.stacked_widget.addWidget(self.posts_page)
        self.stacked_widget.addWidget(self.forgot_password_page)
        self.stacked_widget.addWidget(self.post_page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)
        main_frame.setLayout(main_layout)

        header_layout.addWidget(self.header)
        header_layout.addWidget(main_frame)

        self.sidebar.hide()

        # Navigation events
        self.signin_page.switch_to_Register.connect(lambda: self.change_page(PageIndex.REGISTER))
        self.register_page.switch_to_SignIn.connect(lambda: self.change_page(PageIndex.SIGN_IN))
        self.signin_page.switch_to_ForgotPassword.connect(lambda: self.change_page(PageIndex.FORGOT_PASSWORD))
        self.forgot_password_page.switch_to_SignIn.connect(lambda: self.change_page(PageIndex.SIGN_IN))

        # Colour theme events
        self.signin_page.toggle_btn.clicked.connect(self.toggle_theme)
        self.register_page.toggle_btn.clicked.connect(self.toggle_theme)
        self.forgot_password_page.toggle_btn.clicked.connect(self.toggle_theme)

        # Page events
        self.signin_page.login_btn.clicked.connect(lambda: self.change_page(PageIndex.DASHBOARD))
        self.register_page.login_btn.clicked.connect(lambda: self.change_page(PageIndex.DASHBOARD))
        self.forgot_password_page.login_btn.clicked.connect(lambda: self.change_page(PageIndex.DASHBOARD))
        self.dashboard_page.todo.clicked.connect(lambda: self.change_page(PageIndex.TODO))
        self.dashboard_page.posts.clicked.connect(lambda: self.change_page(PageIndex.POSTS))
        self.posts_page.open_post.clicked.connect(lambda: self.change_page(PageIndex.POST_CONTENT))

        # Header events
        #self.header.account.connect()
        #self.header.settings.connect()
        self.header.log_out.connect(lambda: self.change_page(PageIndex.SIGN_IN))

        # Sidebar events
        self.sidebar.nav_dashboard.connect(lambda: self.change_page(PageIndex.DASHBOARD))
        self.sidebar.nav_todo.connect(lambda: self.change_page(PageIndex.TODO))
        self.sidebar.nav_posts.connect(lambda: self.change_page(PageIndex.POSTS))

        self.apply_theme()

    def change_page(self, index: PageIndex):
        self.stacked_widget.setCurrentIndex(index.value)
        
        # Shows sidebar only when logged in.
        if index in (PageIndex.SIGN_IN, PageIndex.REGISTER, PageIndex.FORGOT_PASSWORD):
            self.sidebar.hide()
        else:
            self.sidebar.show()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        theme_text = "☀️ Light Mode" if self.is_dark_mode else "🌑 Dark Mode"

        self.signin_page.toggle_btn.setText(theme_text)
        self.register_page.toggle_btn.setText(theme_text)

        self.apply_theme()

    def apply_theme(self):
        filename = "dark.qss" if self.is_dark_mode else "light.qss"
        filepath = f"assets/styles/{filename}"
        with open(filepath, "r") as file:
            self.setStyleSheet(file.read())

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())