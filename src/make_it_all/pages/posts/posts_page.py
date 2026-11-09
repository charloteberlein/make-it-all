from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from make_it_all.pages.account.user import get_user_by_id
from make_it_all.pages.base_page import BasePage
from make_it_all.pages.posts.post_content import PostContent
from make_it_all.pages.topics.topic_content import TopicContent
from make_it_all.pages.topics.topic_content_page import TopicFrame


class PostsPage(BasePage):
    post_selected = Signal(str)
    user_id: int | None = None
    showing_mine = False

    def __init__(self):
        super().__init__()

    def define_layout(self) -> None:
        super().define_layout()
        self.top_frame = QFrame()
        self.top_frame.setObjectName("TopBar")

        self.top_bar = QHBoxLayout()

        self.post_frame = QFrame()
        self.post_bar = QHBoxLayout()

        self.recent_layout = QVBoxLayout()

    def define_widgets(self) -> None:
        # Top
        self.title = QLabel("Posts")
        self.title.setObjectName("TitleLabelCenter")
        
        self.my_topics = QPushButton("View Topics")
        self.my_topics.setObjectName("LoginButton")
        self.my_topics.setCursor(Qt.CursorShape.PointingHandCursor)

        # Posts view
        self.make_post = QPushButton("Make a new post")
        self.make_post.setObjectName("LoginButton")
        self.make_post.setCursor(Qt.CursorShape.PointingHandCursor)

        self.my_posts_button = QPushButton("My posts")
        self.my_posts_button.setObjectName("LoginButton")
        self.my_posts_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.my_posts_button.clicked.connect(self.toggle_posts)
        
        self.recent_heading = QLabel("Recent posts")
        self.recent_heading.setObjectName("HeadingLabel")

    def assemble_widgets(self) -> None:
        self.top_bar.addWidget(self.title)
        self.top_frame.setLayout(self.top_bar)

        self.post_bar.addWidget(self.my_topics)
        self.post_bar.addWidget(self.make_post)
        self.post_bar.addWidget(self.my_posts_button)
        self.post_frame.setLayout(self.post_bar)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.top_frame)
        self.layout.addWidget(self.post_frame)

        self.layout.addWidget(self.recent_heading)
        self.layout.addLayout(self.recent_layout)
        self.layout.addStretch()
        self.refresh_recent_posts()

        self.setLayout(self.layout)

    def clear_recent_posts(self) -> None:
        while self.recent_layout.count():
            item = self.recent_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def set_user(self, user_id: int | None) -> None:
        self.user_id = user_id
        self.showing_mine = False
        self.refresh_recent_posts()

    def toggle_posts(self) -> None:
        self.showing_mine = not self.showing_mine
        self.refresh_recent_posts()

    def refresh_recent_posts(self) -> None:
        self.clear_recent_posts()
        if self.showing_mine:
            posts = PostContent.get_posts_by_user(self.user_id)
            self.recent_heading.setText("My Posts")
            self.my_posts_button.setText("Recent posts")
            if not posts:
                self.recent_layout.addWidget(QLabel("You haven't made any posts yet."))
        else:
            posts = PostContent.get_recent_posts(5)
            self.recent_heading.setText("Recent posts")
            self.my_posts_button.setText("My posts")

        for post in posts:
            row = TopicFrame(post.id)
            row.setCursor(Qt.CursorShape.PointingHandCursor)
            row.clicked.connect(self.post_selected)
            row_layout = QHBoxLayout()

            title = QLabel(post.title, alignment=Qt.AlignmentFlag.AlignLeft)
            title.setObjectName("PostTitle") 
            author = get_user_by_id(post.created_by)
            author_name = author.name if author else "Unknown"
            details = QLabel(
                f"{author_name}  .  {TopicContent.get_topic_name(post.topic)}  .  {post.date_created}",
                alignment=Qt.AlignmentFlag.AlignRight,
            )

            row_layout.addWidget(title)
            row_layout.addWidget(details)
            row.setLayout(row_layout)
            self.recent_layout.addWidget(row)

    