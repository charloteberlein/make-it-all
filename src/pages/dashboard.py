from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        self.posts = QPushButton("View posts")
        self.todo = QPushButton("View To-do")

        self.posts.setCursor(Qt.PointingHandCursor)
        self.todo.setCursor(Qt.PointingHandCursor)

        self.widgets = (self.posts, self.todo)