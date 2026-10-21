from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

class BasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.define_styling()
        self.define_layout()
        self.widgets = tuple()
        self.define_widgets()
        self.assemble_widgets()

    def define_styling(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)

    def define_layout(self) -> None:
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(35, 30, 35, 30)
        self.layout.setSpacing(14)

    def define_widgets(self) -> None:
        pass

    def assemble_widgets(self) -> None:
        for widget in self.widgets:
            if isinstance(widget, QWidget) and widget.sizePolicy().horizontalPolicy() == QSizePolicy.Fixed:
                widget.setSizePolicy(QSizePolicy.Expanding, widget.sizePolicy().verticalPolicy())
            self.layout.addWidget(widget)
        self.setLayout(self.layout)