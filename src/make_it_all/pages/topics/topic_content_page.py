from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from make_it_all.data.topics import TopicContent
from make_it_all.pages.base_page import BasePage


class TopicFrame(QFrame):
    clicked = Signal(str)

    def __init__(self, post_id: str):
        super().__init__()
        self.post_id = post_id
        self.setObjectName("Topic")

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self.clicked.emit(self.post_id)


class TopicContentPage(BasePage):
    post_selected = Signal(str)
    back = Signal()
    topic_writable = Signal()

    def __init__(self, topic_id: str = ""):
        self._topic_id = topic_id
        self.writable = TopicContent.get_topic_writable(self.topic_id)
        super().__init__()

    @property
    def topic_id(self) -> str:
        return self._topic_id

    @topic_id.setter
    def topic_id(self, topic_id: str):
        self._topic_id = topic_id
        self.writable = TopicContent.get_topic_writable(topic_id)
        self.toggle_btn.setText("Make Read-Only" if self.writable else "Make Writable")
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

        self.back_btn = QPushButton("⟵")
        self.back_btn.clicked.connect(self.back.emit)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setToolTip("Back to topics")
        self.back_btn.setFixedSize(35, 35)

        self.topic_title = QLabel("")
        self.topic_title.setObjectName("TopicTitle")

        self.toggle_btn = QPushButton("")
        self.toggle_btn.clicked.connect(self.topic_writable.emit)
        self.toggle_btn.setText("Make Read-Only" if self.writable else "Make Writable")
        self.toggle_btn.setObjectName("ToggleButton")
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setVisible(False)

        header_layout.addWidget(self.back_btn)
        header_layout.addWidget(self.topic_title)
        header_layout.addStretch()
        header_layout.addWidget(self.toggle_btn)
        self.header_frame.setLayout(header_layout)

    def define_widgets(self) -> None:
        self.posts = TopicContent.get_posts_by_topic(self.topic_id)

        self.topic_title.setText(TopicContent.get_topic_name(self.topic_id))

        self.widgets = []
        for post in self.posts:
            layout = QHBoxLayout()
            layout_frame = TopicFrame(post.id)
            layout_frame.clicked.connect(self.post_selected)
            layout_frame.setCursor(Qt.CursorShape.PointingHandCursor)

            title = QLabel(post.title, alignment=Qt.AlignmentFlag.AlignLeft)
            title.setObjectName("PostTitle")
            date = QLabel(post.date_created, alignment=Qt.AlignmentFlag.AlignRight)

            layout.addWidget(title)
            layout.addWidget(date)
            layout_frame.setLayout(layout)

            self.widgets.append((layout_frame, post.id))

    def assemble_widgets(self) -> None:
        self.layout.addWidget(self.header_frame)
        for widget, _ in self.widgets:
            self.layout.addWidget(widget)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def toggle_topic_writable(self) -> None:
        self.writable = not self.writable
        self.toggle_btn.setText("Make Read-Only" if self.writable else "Make Writable")
        TopicContent.set_topic_writable(self.topic_id, self.writable)

    def set_can_toggle(self, allowed: bool) -> None:
        self.toggle_btn.setVisible(allowed)
