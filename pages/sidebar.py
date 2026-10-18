from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton

class Sidebar(QFrame):
    nav_dashboard = Signal()
    nav_todo = Signal()
    nav_posts = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.define_styling()
        self.define_layout()
        self.define_widgets()
        self.assemble_widgets()

    def define_styling(self) -> None:
        self.setFixedWidth(70)

    def define_layout(self) -> None:
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(12)

    def define_widgets(self) -> None:
        # Navigation Buttons with tooltips
        self.dashboard_btn = QPushButton("🏡")
        self.dashboard_btn.setToolTip("Dashboard")

        self.todo_btn = QPushButton("📝")
        self.todo_btn.setToolTip("To-Do")

        self.posts_btn = QPushButton("📨")
        self.posts_btn.setToolTip("Posts")

        for btn in (self.dashboard_btn, self.todo_btn, self.posts_btn):
            btn.setObjectName("SideNavButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(50, 50)
            layout.addWidget(btn)

        # Connect buttons to signals
        self.dashboard_btn.clicked.connect(self.nav_dashboard.emit)
        self.todo_btn.clicked.connect(self.nav_todo.emit)
        self.posts_btn.clicked.connect(self.nav_posts.emit)
        
        layout.addStretch()