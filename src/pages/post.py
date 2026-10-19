from pathlib import Path
from PySide6.QtWidgets import QLabel, QTextEdit, QFrame, QHBoxLayout

from helpers import read_json
from pages.base_page import BasePage

class PostContent():
    def __init__(
        self, id: int, viewed: bool, date_created: str, topic: str, title: str, content: str
    ):
        self.id = id
        self.viewed = viewed                # TODO: Add notifications for posts not yet viewed.
        self.date_created = date_created
        self.topic = topic
        self.title = title
        self.content = content

    @classmethod
    def load_posts(cls, filepath: Path | str) -> list["PostContent"]:
        data: list[dict] = read_json(filepath)["posts"]
        posts = []
        for post in data:
            posts.append(cls(
                id=post["metadata"]["id"],
                viewed=True if post["metadata"]["viewed"] else False,
                date_created=post["metadata"]["date-created"],
                topic=post["topic"],
                title=post["title"],
                content=post["content"]
            ))
        return posts
                    

class PostContentPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_layout(self) -> None:
        super().define_layout()

        self.metadata_frame = QFrame()
        self.metadata_frame.setObjectName("TopBar")
        self.metadata_layout = QHBoxLayout()

    def define_widgets(self) -> None:
        post = PostContent.load_posts("assets/mock_data/posts.json")[0]

        self.title = QLabel(post.title)
        self.title.setObjectName("PostTitle")
        self.topic = QLabel(post.topic)
        self.date = QLabel(post.date_created)
        self.content = QTextEdit(post.content)
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