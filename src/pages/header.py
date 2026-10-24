from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel, QMenu

class Header(QFrame):
    account = Signal()
    toggle_theme = Signal()
    log_out = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Header")
        self.define_styling()
        self.define_layout()
        self.define_widgets()
        self.assemble_widgets()

    def define_styling(self) -> None:
        self.setFixedHeight(60)

    def define_layout(self) -> None:
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(12)

    def define_widgets(self) -> None:
        # Header company name
        self.title = QLabel("Make-It-All", alignment=Qt.AlignHCenter)
        self.title.setObjectName("HeaderTitle")

        # Settings dropdown menu icon
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setToolTip("Settings Menu")
        self.settings_btn.setObjectName("SideNavButton")
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.setFixedSize(35, 35)

        self.menu = QMenu(self)

        # Dropdown Items
        self.account_action = self.menu.addAction("👤 Account Details")
        self.theme_action = self.menu.addAction("🌓 Toggle Light/Dark Mode")
        self.menu.addSeparator()
        self.logout_action = self.menu.addAction("↪️ Log Out")

        self.account_action.triggered.connect(self.account.emit)
        self.theme_action.triggered.connect(self.toggle_theme.emit)
        self.logout_action.triggered.connect(self.log_out.emit)

        self.settings_btn.clicked.connect(self.show_settings_menu)

    def show_settings_menu(self):    # Aligns right edge of icon with dropdown
        point = self.settings_btn.mapToGlobal(self.settings_btn.rect().bottomRight())
        menu_width = self.menu.sizeHint().width()
        point.setX(point.x() - menu_width)
        self.menu.exec(point)

    def assemble_widgets(self) -> None:
        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.settings_btn)