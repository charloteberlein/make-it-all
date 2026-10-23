from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from pages.base_page import BasePage

class AccountPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        self.account = QPushButton("Test!! Account!")
        self.account.setCursor(Qt.PointingHandCursor)

        self.widgets = (self.account,)