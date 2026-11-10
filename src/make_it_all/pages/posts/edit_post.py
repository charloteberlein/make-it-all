from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QToolBar,
)

from make_it_all.data.posts import PostContent
from make_it_all.data.topics import TopicContent
from make_it_all.pages.base_page import BasePage


class EditPostPage(BasePage):
    key_pressed = Signal()
    edit = Signal(str)

    def __init__(self, id: str = ""):
        self._id = id
        self.post = PostContent.get_post_by_id(id) or PostContent("", False, "", False, "", "", "")
        super().__init__()

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, new_id: str):
        self._id = new_id
        self.post = PostContent.get_post_by_id(new_id) or PostContent(
            "", False, "", False, "", "", ""
        )

        self.title_input.setText(self.post.title)
        self.topic_options.setCurrentText(TopicContent.get_topic_name(self.post.topic))
        self.date.setText(self.post.date_created)
        self.content.setHtml(self.post.content)

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
        self.title_input.setText(self.post.title)
        self.title_input.textChanged.connect(self.toggle_confirm_btn)

        self.topic_label = QLabel("Topic:")
        self.topic_options = QComboBox()
        self.refresh_topic_options()
        # TODO: Set topic to post topic in the dropdown
        # TODO: (If the topic is changed) check if the previous topic has any posts, otherwise remove that
        self.topic_options.activated.connect(
            lambda _: self.toggle_textbox(self.topic_options.currentText())
        )
        self.topic_input = QLineEdit()
        self.topic_input.hide()
        self.topic_input.textChanged.connect(self.toggle_confirm_btn)

        self.date = QLabel(f"Date created: {self.post.date_created}")

        # Post text editor
        self.toolbar = QToolBar()
        self.content = QTextEdit()
        self.content.setText(self.post.content)
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
            lambda checked: self.content.setFontItalic(True if checked else False)
        )
        self.toolbar.addAction(italic)
        self.toolbar.widgetForAction(italic).setObjectName("ItalicFormatButton")

        underline = QAction("U", self)
        underline.setCheckable(True)
        underline.triggered.connect(
            lambda checked: self.content.setFontUnderline(True if checked else False)
        )
        self.toolbar.addAction(underline)
        self.toolbar.widgetForAction(underline).setObjectName("UnderlineFormatButton")

        # TODO fix later: formatting is forgotten when the user moves the text cursor manually

        self.confirm_btn = QPushButton("Save edits")
        self.confirm_btn.clicked.connect(lambda: self.edit.emit(self.post.id))
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

    def save_post(self) -> None:
        posts = PostContent.load_posts()
        post = next(post for post in posts if post.id == self.post.id)
        initial_topic_id = post.topic
        post.title = self.title_input.text()
        post.topic = TopicContent.get_matching_topic(
            self.topic_input.text() or self.topic_options.currentText()
        )
        post.content = self.content.document().toHtml()

        PostContent.save_posts(posts)
        if post.topic != initial_topic_id:
            TopicContent.remove_topic_if_empty(initial_topic_id)

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
                (  # Valid drop-down topic
                    self.topic_options.currentText() != "Other"
                    and TopicContent.get_topic_writable(
                        TopicContent.get_matching_topic(self.topic_options.currentText())
                    )
                )
                or (  # Valid text input topic
                    len(text := self.topic_input.text()) > 0
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
