from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget


class BasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.define_styling()
        self.define_layout()
        self.widgets = ()
        self.define_widgets()
        self.assemble_widgets()

    def define_styling(self) -> None:
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def define_layout(self) -> None:
        self.page_layout = QVBoxLayout()
        self.page_layout.setContentsMargins(35, 30, 35, 30)
        self.page_layout.setSpacing(14)

    def define_widgets(self) -> None:
        pass

    def assemble_widgets(self) -> None:
        for widget in self.widgets:
            if (
                isinstance(widget, QWidget)
                and widget.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Fixed
            ):
                widget.setSizePolicy(
                    QSizePolicy.Policy.Expanding, widget.sizePolicy().verticalPolicy()
                )
            self.page_layout.addWidget(widget)
        self.setLayout(self.page_layout)
