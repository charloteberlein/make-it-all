from PySide6.QtWidgets import QPushButton, QFrame, QHBoxLayout, QVBoxLayout, QLabel

from pages.base_page import BasePage

class PostsPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_layout(self) -> None:
        super().define_layout()
        self.top_frame = QFrame()
        self.top_frame.setObjectName("TopBar")

        self.top_bar = QHBoxLayout()

        self.post_frame = QFrame()
        self.post_frame.setObjectName("TopBar")
        self.post_bar = QHBoxLayout()

    def define_widgets(self) -> None:
        # Top
        self.title = QLabel("Posts")
        self.title.setObjectName("TitleLabelCenter")
        
        self.my_posts = QPushButton("My Posts")
        self.my_topics = QPushButton("My Topics")

        # Posts view
        self.make_post = QPushButton("Make a new post")
        self.open_post = QPushButton("Open recent post")

    def assemble_widgets(self) -> None:
        self.top_bar.addWidget(self.title)
        self.top_bar.addWidget(self.my_posts)
        self.top_frame.setLayout(self.top_bar)

        self.post_bar.addWidget(self.make_post)
        self.post_bar.addWidget(self.open_post)
        self.post_frame.setLayout(self.post_bar)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.top_frame)
        self.layout.addWidget(self.post_frame)
        
        self.setLayout(self.layout)