from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from pages.base_page import BasePage

class NotificationsPage(BasePage):
    def __init__(self):
        super().__init__()

    def define_widgets(self) -> None:
        self.notifications = QPushButton("Test!! Notifications !")
        self.notifications.setCursor(Qt.PointingHandCursor)

        self.widgets = (self.notifications,)