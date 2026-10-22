from PySide6.QtWidgets import QLabel, QTextEdit, QFrame, QHBoxLayout

from pages.base_page import BasePage
from pages.topics.topics_page import TopicContent
from pages.posts.post_content import PostContent

class PostContentPage(BasePage):
    def __init__(self, id: int = 0):
        self._id = id
        self.post = PostContent.get_post_by_id(id) or PostContent(0, False, "", 0, "", "")
        super().__init__()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id
        self.post = PostContent.get_post_by_id(new_id) or PostContent(0, False, "", 0, "", "")
        topics = TopicContent.load_topics("assets/mock_data/topics.json")
        
        self.title.setText(self.post.title)
        self.topic.setText(topics[self.post.topic].name)
        self.date.setText(self.post.date_created)
        self.content.setHtml(self.post.content)

    def define_layout(self) -> None:
        super().define_layout()

        self.metadata_frame = QFrame()
        self.metadata_frame.setObjectName("TopBar")
        self.metadata_layout = QHBoxLayout()

    def define_widgets(self) -> None:
        topics = TopicContent.load_topics("assets/mock_data/topics.json")

        self.title = QLabel(self.post.title)
        self.title.setObjectName("PostTitle")
        self.topic = QLabel(topics[self.post.topic].name)
        self.date = QLabel(self.post.date_created)
        self.content = QTextEdit()
        self.content.setHtml(self.post.content)
        self.content.setReadOnly(True)

    def assemble_widgets(self) -> None:
        # Metadata (under title)
        self.metadata_layout.addWidget(self.topic)
        self.metadata_layout.addWidget(self.date)
        self.metadata_layout.addStretch()
        self.metadata_frame.setLayout(self.metadata_layout)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.metadata_frame)
        self.layout.addWidget(self.content)
        
        self.setLayout(self.layout)
        