from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel

class Header(QFrame):
    account = Signal()
    settings = Signal()
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

        # Navigation Buttons with tooltips
        self.account_btn = QPushButton("👤")
        self.account_btn.setToolTip("Account")

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setToolTip("Settings")

        self.log_out_btn = QPushButton("↪️")
        self.log_out_btn.setToolTip("Log out")

        for btn in (self.account_btn, self.settings_btn, self.log_out_btn):
            btn.setObjectName("SideNavButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(40, 40)

        # Connect buttons to signals
        self.account_btn.clicked.connect(self.account.emit)
        self.settings_btn.clicked.connect(self.settings.emit)
        self.log_out_btn.clicked.connect(self.log_out.emit)

    def assemble_widgets(self) -> None:
        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.log_out_btn)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.settings_btn)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.account_btn)