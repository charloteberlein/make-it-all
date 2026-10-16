from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from pages.base_page import BasePage

class TodoPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        self.todo = QPushButton("Test!! TODO!")
        self.todo.setCursor(Qt.PointingHandCursor)

        self.widgets = (self.todo,)