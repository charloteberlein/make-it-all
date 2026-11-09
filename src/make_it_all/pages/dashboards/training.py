from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from make_it_all.helpers import DATA_DIR
from make_it_all.pages.base_page import BasePage
from make_it_all.pages.posts.post_content import PostContent
from make_it_all.pages.topics.topic_content import TopicContent


class TrainingPage(BasePage):
    to_Dashboard = Signal()

    def __init__(self, current_user = None):
        super().__init__()
        self.current_user = current_user

    def define_layout(self) -> None:
        super().define_layout()
        self.title_frame = QFrame()
        self.title_layout = QHBoxLayout(self.title_frame)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.refresh_recommendations()

    def define_widgets(self) -> None:
        self.heading = QLabel("Recommended Training Areas")
        self.heading.setObjectName("HeadingLabel")

        self.subheading = QLabel("High-priority training modules based on employee upvotes on posts.")
        self.subheading.setObjectName("SubheadingLabel")
        self.subheading.setContentsMargins(9, 0, 9, 0)

        self.back_btn = QPushButton("◀️ Back to Dashboard")
        self.back_btn.setObjectName("NavButton")
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setFixedWidth(200)
        self.back_btn.clicked.connect(self.to_Dashboard.emit)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)

        self.container_widget = QWidget()
        self.card_layout = QVBoxLayout(self.container_widget)
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.card_layout.setSpacing(10)
        self.scroll_area.setWidget(self.container_widget)

    def assemble_widgets(self) -> None:
        self.title_layout.addWidget(self.heading)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.layout.addWidget(self.title_frame)
        self.layout.addWidget(self.subheading)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.container_widget)
        self.layout.addSpacing(14)
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.refresh_recommendations()

    def refresh_recommendations(self) -> None:
        posts = PostContent.load_posts(DATA_DIR / "posts.json")
        sorted_posts = sorted(posts, key = lambda posts: int(posts.upvote_count), reverse=True)

        # Clear existing cards.
        while self.card_layout.count():
            child = self.card_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        top_posts = sorted_posts[:2]

        # Builds card for top posts.
        for post in top_posts:
            card = QFrame()
            card.setObjectName("PostCard")
            card_layout = QHBoxLayout(card)

            info_layout = QVBoxLayout()
            title_label = QLabel(post.title)
            
            topic_name = TopicContent.get_topic_name(post.topic)
            topic_label = QLabel(f"Topic: {topic_name}")
            topic_label.setObjectName("SubheadingLabel")

            info_layout.addWidget(title_label)
            info_layout.addWidget(topic_label)

            upvote_label = QLabel(f"👍 {post.upvote_count} Upvotes")
            upvote_label.setAlignment(Qt.AlignCenter)

            card_layout.addLayout(info_layout, stretch = 2)
            card_layout.addWidget(upvote_label, stretch = 1, alignment = Qt.AlignRight)

            self.card_layout.addWidget(card)

        self.card_layout.addStretch()