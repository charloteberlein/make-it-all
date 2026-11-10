from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton

from make_it_all.data.topics import TopicContent
from make_it_all.pages.base_page import BasePage


class TopicsPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        self.title = QLabel("Topics")
        self.title.setObjectName("TitleLabelCenter")

        self.topics = TopicContent.load_topics()
        self.widgets = []
        for topic in self.topics:
            btn = QPushButton(topic.name)
            btn.setObjectName("LoginButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.widgets.append((btn, topic.id))

    def assemble_widgets(self) -> None:
        self.page_layout.addWidget(self.title)
        for widget, _ in self.widgets:
            self.page_layout.addWidget(widget)
        self.page_layout.addStretch()

        self.setLayout(self.page_layout)

    def refresh_topics(self):
        for widget, _ in self.widgets:
            widget.deleteLater()
        self.widgets = []

        self.topics = TopicContent.load_topics()
        for topic in self.topics:
            btn = QPushButton(topic.name)
            btn.setObjectName("LoginButton")
            self.widgets.append((btn, topic.id))

        self.assemble_widgets()
