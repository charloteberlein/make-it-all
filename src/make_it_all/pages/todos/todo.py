from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QPushButton

from make_it_all.pages.base_page import BasePage


class TodoPage(BasePage):
    to_Personal_Todo = Signal()
    to_Project_Todo = Signal()

    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        self.title = QLabel("My To-do Lists")
        self.title.setObjectName("HeadingLabel")
        self.title.setAlignment(Qt.AlignCenter)

        self.personal_btn = QPushButton("☑️ Personal To-do List")
        self.personal_btn.setObjectName("ToDoButton")
        self.personal_btn.setCursor(Qt.PointingHandCursor)
        self.personal_btn.setFixedWidth(450)
        self.personal_btn.clicked.connect(self.to_Personal_Todo.emit)

        self.project_btn = QPushButton("📋 Project To-do List")
        self.project_btn.setObjectName("ToDoButton")
        self.project_btn.setCursor(Qt.PointingHandCursor)
        self.project_btn.setFixedWidth(450)
        self.project_btn.clicked.connect(self.to_Project_Todo.emit)

    def assemble_widgets(self) -> None:
        # Landing page.
        self.layout.addStretch(1)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.personal_btn, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.project_btn, alignment=Qt.AlignCenter)
        self.layout.addStretch(1)

        self.setLayout(self.layout)
