from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMenu, QPushButton

from make_it_all.data.notifications import get_notifications, mark_all_read
from make_it_all.data.user import User


class Header(QFrame):
    account = Signal()
    toggle_theme = Signal()
    log_out = Signal()
    open_todo = Signal(str)

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
        self.page_layout = QHBoxLayout(self)
        self.page_layout.setContentsMargins(10, 15, 10, 15)
        self.page_layout.setSpacing(12)

    def define_widgets(self) -> None:
        # Header company name
        self.title = QLabel("Make-It-All", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.title.setObjectName("HeaderTitle")

        # Settings dropdown menu icon
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setToolTip("Settings Menu")
        self.settings_btn.setObjectName("SideNavButton")
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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

        # Notification Bell
        self.user: User | None = None
        self.bell_btn = QPushButton("🔔")
        self.bell_btn.setToolTip("Notifications")
        self.bell_btn.setObjectName("SideNavButton")
        self.bell_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bell_btn.setFixedSize(35, 35)
        self.bell_btn.setVisible(False)
        self.badge = QLabel("", self.bell_btn)
        self.badge.setObjectName("BellBadge")
        self.badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.badge.setFixedSize(16, 16)
        self.badge.move(19, 0)
        self.badge.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.badge.hide()
        self.bell_btn.clicked.connect(self.show_notifications)

    def show_settings_menu(self):  # Aligns right edge of icon with dropdown
        point = self.settings_btn.mapToGlobal(self.settings_btn.rect().bottomRight())
        menu_width = self.menu.sizeHint().width()
        point.setX(point.x() - menu_width)
        self.menu.exec(point)

    def set_user(self, user: User | None) -> None:
        self.user = user
        self.bell_btn.setVisible(user is not None)
        self.refresh_bell()

    def refresh_bell(self) -> None:
        unread = 0
        if self.user:
            unread = len([n for n in get_notifications(self.user) if not n.read])
        self.badge.setText(str(unread))
        self.badge.setVisible(unread > 0)

    def show_notifications(self) -> None:
        if self.user is None:
            return

        user = self.user
        menu = QMenu(self)
        notifications = get_notifications(user)
        if not notifications:
            menu.addAction("No notifications").setEnabled(False)
        for notification in notifications:
            dot = "" if notification.read else "● "
            action = menu.addAction(dot + notification.message)
            action.triggered.connect(
                lambda checked=False, task_type=notification.task_type: self.open_todo.emit(
                    task_type
                )
            )

        point = self.bell_btn.mapToGlobal(self.bell_btn.rect().bottomRight())
        point.setX(point.x() - menu.sizeHint().width())
        menu.exec(point)

        mark_all_read(user)
        self.refresh_bell()

    def assemble_widgets(self) -> None:
        self.page_layout.addWidget(self.title)
        self.page_layout.addStretch()
        self.page_layout.addWidget(self.bell_btn)
        self.page_layout.addWidget(self.settings_btn)
