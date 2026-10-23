from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QPushButton, QFrame, QHBoxLayout, QVBoxLayout, QLabel

from pages.base_page import BasePage
from pages.posts.post_content import PostContent
from pages.topics.topic_content import TopicContent
from pages.topics.topic_content_page import TopicFrame

class PostsPage(BasePage):
    post_selected = Signal(int)

    def __init__(self):
        super().__init__()

    def define_layout(self) -> None:
        super().define_layout()
        self.top_frame = QFrame()
        self.top_frame.setObjectName("TopBar")

        self.top_bar = QHBoxLayout()

        self.post_frame = QFrame()
        self.post_frame.setObjectName("TopBar")
        self.post_bar = QHBoxLayout()
        self.recent_layout = QVBoxLayout()

    def define_widgets(self) -> None:
        # Top
        self.title = QLabel("Posts")
        self.title.setObjectName("TitleLabelCenter")
        
        self.my_topics = QPushButton("View Topics")
        self.my_topics.setObjectName("LoginButton")

        # Posts view
        self.make_post = QPushButton("Make a new post")
        self.make_post.setObjectName("LoginButton")
        self.recent_heading = QLabel("Recent posts")
        self.recent_heading.setObjectName("HeadingLabel")

    def assemble_widgets(self) -> None:
        self.top_bar.addWidget(self.title)
        self.top_bar.addWidget(self.my_topics)
        self.top_frame.setLayout(self.top_bar)

        self.post_bar.addWidget(self.make_post)
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

    def refresh_recent_posts(self) -> None:
        self.clear_recent_posts()
        topics = TopicContent.load_topics("assets/mock_data/topics.json")

        for post in PostContent.get_recent_posts(5):
            row = TopicFrame(post.id)
            row.clicked.connect(self.post_selected)
            row_layout = QHBoxLayout()

            title = QLabel(post.title, alignment=Qt.AlignmentFlag.AlignLeft)
            title.setObjectName("PostTitle") 
            details = QLabel(
                f"{topics[post.topic].name}  .  {post.date_created}",
                alignment=Qt.AlignmentFlag.AlignRight,
            )

            row_layout.addWidget(title)
            row_layout.addWidget(details)
            row.setLayout(row_layout)
            self.recent_layout.addWidget(row)

    