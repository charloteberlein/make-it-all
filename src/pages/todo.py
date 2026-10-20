from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from src.pages.base_page import BasePage

class TodoPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        # Navigation
        self.top_frame = QFrame()
        self.top_frame.setObjectName("TopBar")

        self.top_bar = QHBoxLayout()
        self.top_bar.addStretch()

        self.title = QLabel("Make-It-All")
        self.title.setObjectName("TitleLabelCenter")
        self.top_bar.addWidget(self.title)
        self.top_frame.setLayout(self.top_bar)

    def assemble_widgets(self) -> None:
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.top_frame)
        
        self.setLayout(self.layout)
