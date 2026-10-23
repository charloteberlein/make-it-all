from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QLabel, QComboBox, QTextEdit, QFrame, QHBoxLayout, QLineEdit, QPushButton, QToolBar
)
from datetime import datetime as dt

from helpers import read_json, write_json
from pages.base_page import BasePage
from pages.topics.topic_content import TopicContent

class MakePostPage(BasePage):
    key_pressed = Signal()

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
        self.title_input.textChanged.connect(self.toggle_confirm_btn)

        self.topic_label = QLabel("Topic:")
        self.topic_options = QComboBox()
        self.refresh_topic_options()
        self.topic_options.activated.connect(
            lambda _: self.toggle_textbox(self.topic_options.currentText())
        )
        self.topic_input = QLineEdit()
        self.topic_input.hide()
        self.topic_input.textChanged.connect(self.toggle_confirm_btn)

        self.date = QLabel(f"Date created: {self.date_created}")

        # Post text editor
        self.toolbar = QToolBar()
        self.content = QTextEdit()
        self.content.textChanged.connect(self.toggle_confirm_btn)

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
        self.confirm_btn.setEnabled(False)

    def assemble_widgets(self) -> None:
        # Title
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.title_input)
        self.title_frame.setLayout(self.title_layout)

        # Metadata (under title)
        self.metadata_layout.addWidget(self.topic_label)
        self.metadata_layout.addWidget(self.topic_options)
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

    def toggle_textbox(self, option: str):
        self.toggle_confirm_btn()
        if option == "Other":
            self.topic_input.show()
        else:
            self.topic_input.hide()
            self.topic_input.clear()

    def check_post_valid(self) -> bool:
        return (
            # Title not empty
            len(self.title_input.text()) > 0
            # Topic valid and not empty
            and (
                ( # Valid drop-down topic
                    self.topic_options.currentText() != "Other"
                    and TopicContent.get_topic_writable(
                        TopicContent.get_matching_topic(self.topic_options.currentText())
                    )
                ) or ( # Valid text input topic
                    len((text := self.topic_input.text())) > 0
                    and text != "Other"
                    and text not in [topic.name for topic in TopicContent.load_topics()]
                )
            )
             # Content not empty
            and len(self.content.toPlainText()) > 0
        )

    def toggle_confirm_btn(self) -> None:
        if self.check_post_valid():
            self.confirm_btn.setEnabled(True)
        else:
            self.confirm_btn.setEnabled(False)

    def refresh_topic_options(self) -> None:
        self.topic_options.clear()
        self.topic_options.addItems([topic.name for topic in TopicContent.get_writable_topics()])
        self.topic_options.addItem("Other")