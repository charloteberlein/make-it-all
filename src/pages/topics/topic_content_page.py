from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QHBoxLayout, QFrame, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal

from pages.base_page import BasePage
from pages.topics.topic_content import TopicContent

class TopicFrame(QFrame):
    clicked = Signal(int)

    def __init__(self, post_id: int):
        super().__init__()
        self.post_id = post_id
        self.setObjectName("Topic")

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self.clicked.emit(self.post_id)


class TopicContentPage(BasePage):
    post_selected = Signal(int)
    back = Signal()

    def __init__(self, topic_id: int = 0):
        self._topic_id = topic_id
        super().__init__()

    @property
    def topic_id(self):
        return self._topic_id

    @topic_id.setter
    def topic_id(self, id: int):
        self._topic_id = id
        for widget, _ in self.widgets:
            self.layout.removeWidget(widget)
            widget.deleteLater()

        self.define_widgets()
        for index, (widget, _) in enumerate(self.widgets):
            self.layout.insertWidget(index + 1, widget)

    def define_layout(self) -> None:
        self.layout = QVBoxLayout()

        self.header_frame = QFrame()
        self.header_frame.setObjectName("TopBar")
        header_layout = QHBoxLayout()

        self.back_btn = QPushButton("Back to topics")
        self.back_btn.clicked.connect(self.back.emit)

        self.topic_title = QLabel("")
        self.topic_title.setObjectName("PostTitle")

        header_layout.addWidget(self.back_btn)
        header_layout.addWidget(self.topic_title)
        header_layout.addStretch()
        self.header_frame.setLayout(header_layout)

    def define_widgets(self) -> None:
        self.posts = TopicContent.get_posts_by_topic(self.topic_id)

        topics = TopicContent.load_topics("assets/mock_data/topics.json")
        self.topic_title.setText(topics[self.topic_id].name)

        self.widgets = []
        for post in self.posts:
            layout = QHBoxLayout()
            layout_frame = TopicFrame(post.id)
            layout_frame.clicked.connect(self.post_selected)

            title = QLabel(post.title, alignment=Qt.AlignmentFlag.AlignLeft)
            title.setObjectName("PostTitle")
            date = QLabel(post.date_created, alignment=Qt.AlignmentFlag.AlignRight)

            layout.addWidget(title)
            layout.addWidget(date)
            layout_frame.setLayout(layout)

            self.widgets.append((layout_frame, post.id))

    def assemble_widgets(self) -> None:
        self.layout.addWidget(self.header_frame)
        for (widget, _) in self.widgets:
            self.layout.addWidget(widget)
        self.layout.addStretch()

        self.setLayout(self.layout)