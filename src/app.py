import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout, QFrame
)

from pages.page_index import PageIndex
from pages.header import Header
from pages.sidebar import Sidebar
from pages.dashboard import DashboardPage
from pages.todo import TodoPage

from pages.forgotpassword import ForgotPasswordPage
from pages.my_account import MyAccountPage
from pages.make_post import MakePostPage

from pages.account.signin import SignInPage
from pages.account.register import RegisterPage
from pages.account.forgotpassword import ForgotPasswordPage

from pages.posts.posts_page import PostsPage
from pages.posts.post_content_page import PostContentPage
from pages.posts.make_post import MakePostPage

from pages.topics.topics_page import TopicsPage
from pages.topics.topic_content_page import TopicContentPage

from pages.my_account import MyAccountPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Make-It-All Prototype")
        self.resize(1200, 800)         # Allows for resizing the window.
        self.setMinimumSize(900, 600)

        self.is_dark_mode = False
        self.current_user = None

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
        self.forgot_password_page = ForgotPasswordPage()
        self.dashboard_page = DashboardPage()
        self.todo_page = TodoPage()
        self.posts_page = PostsPage()
        self.post_page = PostContentPage()
        self.make_post_page = MakePostPage()
        self.topics_page = TopicsPage()
        self.topic_content_page = TopicContentPage()
        self.account_page = MyAccountPage()

        self.stacked_widget.addWidget(self.signin_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.forgot_password_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.todo_page)
        self.stacked_widget.addWidget(self.posts_page)
        self.stacked_widget.addWidget(self.post_content_page)
        self.stacked_widget.addWidget(self.make_post_page)
        self.stacked_widget.addWidget(self.topics_page)
        self.stacked_widget.addWidget(self.topic_content_page)
        self.stacked_widget.addWidget(self.account_page)


        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)
        main_frame.setLayout(main_layout)

        header_layout.addWidget(self.header)
        header_layout.addWidget(main_frame)

        self.sidebar.hide()
        self.header.hide()

        # Navigation events
        self.signin_page.switch_to_Register.connect(lambda: self.change_page(PageIndex.REGISTER))
        self.register_page.switch_to_SignIn.connect(lambda: self.change_page(PageIndex.SIGN_IN))
        self.signin_page.switch_to_ForgotPassword.connect(lambda: self.change_page(PageIndex.FORGOT_PASSWORD))
        self.forgot_password_page.switch_to_SignIn.connect(lambda: self.change_page(PageIndex.SIGN_IN))
        self.account_page.switch_to_ForgotPassword.connect(lambda: self.change_page(PageIndex.FORGOT_PASSWORD))

        # Colour theme events
        self.signin_page.toggle_btn.clicked.connect(self.toggle_theme)
        self.register_page.toggle_btn.clicked.connect(self.toggle_theme)
        self.forgot_password_page.toggle_btn.clicked.connect(self.toggle_theme)

        # Page events
        self.signin_page.login_success.connect(self.log_in)
        self.register_page.login_btn.clicked.connect(lambda: self.change_page(PageIndex.DASHBOARD))
        self.forgot_password_page.login_btn.clicked.connect(lambda: self.change_page(PageIndex.DASHBOARD))
        self.dashboard_page.todo.clicked.connect(lambda: self.change_page(PageIndex.TODO))
        self.dashboard_page.posts.clicked.connect(lambda: self.change_page(PageIndex.POSTS))
        self.posts_page.make_post.clicked.connect(lambda: self.change_page(PageIndex.MAKE_POST))
        self.posts_page.my_topics.clicked.connect(lambda: self.change_page(PageIndex.TOPICS))
        self.make_post_page.confirm_btn.clicked.connect(lambda: self.save_and_exit_post_maker())
        self.posts_page.post_selected.connect(self.view_post)

        for (widget, id) in self.topics_page.widgets:
            widget.clicked.connect(
                lambda checked=False, topic_id=id: self.view_topic_posts(topic_id)
            )

        self.topic_content_page.post_selected.connect(self.view_post)
        self.topic_content_page.back.connect(lambda: self.change_page(PageIndex.TOPICS))


        # Header events
        self.header.account.connect(lambda: self.change_page(PageIndex.MY_ACCOUNT))
        self.header.toggle_theme.connect(self.toggle_theme)
        self.header.log_out.connect(self.log_out)

        # Sidebar events
        self.sidebar.nav_dashboard.connect(lambda: self.change_page(PageIndex.DASHBOARD))
        self.sidebar.nav_todo.connect(lambda: self.change_page(PageIndex.TODO))
        self.sidebar.nav_posts.connect(lambda: self.change_page(PageIndex.POSTS))

        self.apply_theme()

    def change_page(self, index: PageIndex):
        self.stacked_widget.setCurrentIndex(index.value)
        
        # Shows sidebar only when logged in.
        if index.value > 2:
            self.sidebar.show()
            self.header.show()
        else:
            self.sidebar.hide()
            self.header.hide()

        if index == PageIndex.POSTS:
            self.posts_page.refresh_recent_posts()

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

    def save_and_exit_post_maker(self):
        user_id = self.current_user.id if self.current_user else None
        self.make_post_page.save_post_to_json(created_by=user_id)
        self.topics_page.refresh_topics()
        for (widget, id) in self.topics_page.widgets:
            widget.clicked.connect(
                lambda checked=False, topic_id=id: self.view_topic_posts(topic_id)
            )
        self.change_page(PageIndex.POSTS)

    def view_post(self, post_id):
        self.post_content_page.id = post_id
        self.change_page(PageIndex.POST_CONTENT)

    def log_in(self, user):
        self.current_user = user
        self.change_page(PageIndex.DASHBOARD)

    def log_out(self):
        self.current_user = None
        self.change_page(PageIndex.SIGN_IN)

    def view_topic_posts(self, topic_id):
        self.topic_content_page.topic_id = topic_id
        self.change_page(PageIndex.TOPIC_CONTENT)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())