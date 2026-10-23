from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from pages.base_page import BasePage

class TrainingPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        self.training = QPushButton("Test!! Training!")
        self.training.setCursor(Qt.PointingHandCursor)

        self.widgets = (self.training,)