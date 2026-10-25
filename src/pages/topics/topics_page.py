from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QLabel

from pages.base_page import BasePage
from pages.topics.topic_content import TopicContent

class TopicsPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        self.title = QLabel("Topics")
        self.title.setObjectName("TitleLabelCenter")

        self.topics = TopicContent.load_topics("assets/mock_data/topics.json")
        self.widgets = []
        for topic in self.topics:
            btn = QPushButton(topic.name)
            btn.setObjectName("LoginButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.widgets.append((btn, topic.id))

    def assemble_widgets(self) -> None:
        self.layout.addWidget(self.title)

        for (widget, _) in self.widgets:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)

    def refresh_topics(self):
        for (widget, _) in self.widgets:
            widget.deleteLater()
        self.widgets = []

        self.topics = TopicContent.load_topics("assets/mock_data/topics.json")
        for topic in self.topics:
            btn = QPushButton(topic.name)
            btn.setObjectName("LoginButton")
            self.widgets.append((btn, topic.id))
        
        self.assemble_widgets()