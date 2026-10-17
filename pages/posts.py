from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from pages.base_page import BasePage

class PostsPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        self.test = QPushButton("Test!!")
        self.test.setCursor(Qt.PointingHandCursor)

        self.widgets = (self.test,)