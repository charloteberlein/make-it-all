from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QTextEdit,
)

from make_it_all.data.posts import PostContent
from make_it_all.data.topics import TopicContent
from make_it_all.pages.base_page import BasePage


class PostContentPage(BasePage):
    back = Signal()
    edit = Signal(str)
    delete = Signal(str)

    def __init__(self, id: str = ""):
        self._id = id
        self.post = PostContent.get_post_by_id(id) or PostContent("", False, "", False, "", "", "")
        self.locked = (
            True if self.post.archived
            or not TopicContent.get_topic_writable(self.post.topic)
            else False
        )
        super().__init__()

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, new_id: str):
        self._id = new_id
        self.post = PostContent.get_post_by_id(new_id) or PostContent("", False, "", False, "", "", "")
        
        self.title.setText(self.post.title)
        self.back_btn.setToolTip(
            f"Back to {TopicContent.get_topic_name(self.post.topic) or "topic"}"
        )
        self.topic.setText(TopicContent.get_topic_name(self.post.topic))
        self.date.setText(self.post.date_created)
        self.content.setHtml(self.post.content)
        self.refresh_upvote_button()

        self.locked = (
            True if self.post.archived
            or not TopicContent.get_topic_writable(self.post.topic)
            else False
        )

        self.edit_stack.setCurrentIndex(int(self.locked))

        self.archive_btn.setText("Unarchive post" if self.post.archived else "Archive post")
        if TopicContent.get_topic_writable(self.post.topic):
            self.archive_btn.show()
        else:
            self.archive_btn.hide()

    def define_layout(self) -> None:
        super().define_layout()

        self.title_frame = QFrame()
        self.title_layout = QHBoxLayout()

        self.edit_frame = QFrame()
        self.edit_layout = QHBoxLayout()
        self.edit_stack = QStackedWidget()
        self.edit_stack.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.metadata_frame = QFrame()
        self.metadata_frame.setObjectName("TopBar")
        self.metadata_layout = QHBoxLayout()

    def define_widgets(self) -> None:
        self.back_btn = QPushButton("⟵")
        self.back_btn.clicked.connect(self.back.emit)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setToolTip(
            f"Back to {TopicContent.get_topic_name(self.post.topic) or "topic"}"
        )
        self.back_btn.setFixedSize(35, 35)

        self.title = QLabel(self.post.title)
        self.title.setObjectName("PostTitle")

        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setObjectName("SideNavButton")
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.clicked.connect(lambda: self.edit.emit(self.post.id))
        self.edit_btn.setToolTip("Edit post")
        self.edit_btn.setFixedSize(35, 35)

        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setObjectName("SideNavButton")
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.clicked.connect(lambda: self.delete.emit(self.post.id))
        self.delete_btn.setToolTip("Delete post")
        self.delete_btn.setFixedSize(35, 35)

        self.archive_btn = QPushButton("Unarchive post" if self.post.archived else "Archive post")
        self.archive_btn.clicked.connect(self.toggle_archive_post)
        self.archive_btn.setObjectName("ToggleButton")
        self.archive_btn.setCursor(Qt.PointingHandCursor)
        if TopicContent.get_topic_writable(self.post.topic):
            self.archive_btn.show()
        else:
            self.archive_btn.hide()

        self.locked_label = QLabel("Locked", alignment=Qt.AlignmentFlag.AlignRight)

        self.upvote_btn = QPushButton(f"👍 Upvote ({self.post.upvote_count})")
        self.upvote_btn.setObjectName("PinkNavButton")
        self.upvote_btn.setCursor(Qt.PointingHandCursor)
        self.upvote_btn.clicked.connect(self.upvote_clicked)
        self.upvote_btn.setCheckable(True)

        self.topic = QLabel(TopicContent.get_topic_name(self.post.topic))
        self.date = QLabel(self.post.date_created)

        self.content = QTextEdit()
        self.content.setHtml(self.post.content)
        self.content.setReadOnly(True)

    def assemble_widgets(self) -> None:
        # Title
        self.edit_layout.addStretch()
        self.edit_layout.addWidget(self.edit_btn)
        self.edit_layout.addWidget(self.delete_btn)
        self.edit_frame.setLayout(self.edit_layout)

        self.edit_stack.addWidget(self.edit_frame)
        self.edit_stack.addWidget(self.locked_label)

        self.edit_stack.setCurrentIndex(int(self.locked))

        self.title_layout.addWidget(self.back_btn)
        self.title_layout.addWidget(self.title)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.edit_stack)
        self.title_frame.setLayout(self.title_layout)

        # Metadata
        self.metadata_layout.addWidget(self.topic)
        self.metadata_layout.addWidget(self.date)
        self.metadata_layout.addStretch()
        self.metadata_layout.addWidget(self.upvote_btn)
        self.metadata_layout.addWidget(self.archive_btn)
        self.metadata_frame.setLayout(self.metadata_layout)

        self.layout.addWidget(self.title_frame)
        self.layout.addWidget(self.metadata_frame)
        self.layout.addWidget(self.content)
        
        self.setLayout(self.layout)

    def toggle_archive_post(self):
        self.post.archived = not self.post.archived
        self.archive_btn.setText("Unarchive post" if self.post.archived else "Archive post")
        PostContent.archive_post(self.post.id, self.post.archived)

        self.locked = not self.locked
        self.edit_stack.setCurrentIndex(int(self.locked))

    def upvote_clicked(self):
        current_user = getattr(self.window(), "current_user", None)
        if not current_user:
            return
        
        new_count, is_upvoted = PostContent.upvote_post(self.post.id, current_user.id)
        self.post.upvote_count = new_count
        if is_upvoted:
            if current_user.id not in self.post.upvoted_users:
                self.post.upvoted_users.append(current_user.id)
        else:
            if current_user.id in self.post.upvoted_users:
                self.post.upvoted_users.remove(current_user.id)

        self.refresh_upvote_button()

    def refresh_upvote_button(self):
        current_user = getattr(self.window(), "current_user", None)
        is_upvoted = current_user and current_user.id in self.post.upvoted_users
        self.upvote_btn.setChecked(bool(is_upvoted))
        self.upvote_btn.setText(f"👍 Upvote ({self.post.upvote_count})")
