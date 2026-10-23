from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QLabel, QTextEdit, QFrame, QHBoxLayout, QLineEdit, QPushButton, QToolBar
from datetime import datetime as dt

from helpers import read_json, write_json
from pages.base_page import BasePage
from pages.topics.topic_content import TopicContent

class MakePostPage(BasePage):
    def __init__(self):
        self.update_date()
        super().__init__()

    def update_date(self):
        self.date_created = dt.today().strftime("%d-%m-%Y")

    def define_layout(self) -> None:
        super().define_layout()

        self.title_frame = QFrame()
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)

        self.metadata_frame = QFrame()
        self.metadata_frame.setObjectName("TopBar")
        self.metadata_layout = QHBoxLayout()
        self.metadata_layout.setContentsMargins(0, 0, 0, 20)

        self.button_frame = QFrame()
        self.button_layout = QHBoxLayout()

    def define_widgets(self) -> None:
        self.title_label = QLabel("Title:")
        self.title_label.setObjectName("PostTitle")
        self.title_input = QLineEdit()

        self.topic_label = QLabel("Topic:")
        self.topic_input = QLineEdit()
        # TODO: Add a drop-down instead of / in addition to the free-text box to prevent typos

        self.date = QLabel(f"Date created: {self.date_created}")

        # Post text editor
        self.toolbar = QToolBar()
        self.content = QTextEdit()

        bold = QAction("B", self)
        bold.setCheckable(True)
        bold.triggered.connect(
            lambda checked: self.content.setFontWeight(
                QFont.Weight.Bold if checked else QFont.Weight.Normal
            )
        )
        self.toolbar.addAction(bold)
        self.toolbar.widgetForAction(bold).setObjectName("BoldFormatButton")

        italic = QAction("I", self)
        italic.setCheckable(True)
        italic.triggered.connect(
            lambda checked: self.content.setFontItalic(
                True if checked else False
            )
        )
        self.toolbar.addAction(italic)
        self.toolbar.widgetForAction(italic).setObjectName("ItalicFormatButton")

        underline = QAction("U", self)
        underline.setCheckable(True)
        underline.triggered.connect(
            lambda checked: self.content.setFontUnderline(
                True if checked else False
            )
        )
        self.toolbar.addAction(underline)
        self.toolbar.widgetForAction(underline).setObjectName("UnderlineFormatButton")

        # TODO fix later: formatting is forgotten when the user moves the text cursor manually

        self.confirm_btn = QPushButton("Create post")
        self.confirm_btn.setObjectName("LoginButton")

    def assemble_widgets(self) -> None:
        # Title
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.title_input)
        self.title_frame.setLayout(self.title_layout)

        # Metadata (under title)
        self.metadata_layout.addWidget(self.topic_label)
        self.metadata_layout.addWidget(self.topic_input)
        self.metadata_layout.addWidget(self.date)
        self.metadata_layout.addStretch()
        self.metadata_frame.setLayout(self.metadata_layout)

        # Button
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.confirm_btn)
        self.button_frame.setLayout(self.button_layout)

        # Main layout
        self.layout.addWidget(self.title_frame)
        self.layout.addWidget(self.metadata_frame)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.content)
        self.layout.addWidget(self.button_frame)
        
        self.setLayout(self.layout)

    def save_post_to_json(self, created_by: int | None = None) -> None:
        """Appends a post to the `posts.json` file."""
        # TODO: Disallow empty titles/topics/content
        data: dict = read_json("assets/mock_data/posts.json")

        self.update_date()
        data["posts"].append(
            {
                "metadata": {
                    "id": data["posts"][-1]["metadata"]["id"] + 1,
                    "viewed": False,
                    "date-created": self.date_created,
                },
                "topic": TopicContent.get_matching_topic(self.topic_input.text()),
                "created_by": created_by,
                "title": self.title_input.text(),
                "content": self.content.document().toHtml(),
            }
        )

        write_json("assets/mock_data/posts.json", data)

        self.title_input.clear()
        self.topic_input.clear()
        self.content.clear()
