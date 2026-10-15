import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QStackedWidget)
# from PySide6.QtCore import Qt
from pages.signin import SignInPage
from pages.register import RegisterPage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Make-It-All Demo")
        self.setFixedSize(380, 420)

        # Sets initial theme to light.
        self.is_dark_mode = False

        # Set up container, and its size.
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Initialise QStackedWidget
        self.stacked_widget = QStackedWidget()
        
        # Instantiate the .py file pages.
        self.signin_page = SignInPage()
        self.register_page = RegisterPage()

        # Add pages to the stack, uses indexes in a switch-case like manner.
        self.stacked_widget.addWidget(self.signin_page)
        self.stacked_widget.addWidget(self.register_page) # can add to the list as we go.

        # Used to pin the stacked Widgets to the main window.
        main_layout.addWidget(self.stacked_widget)

        # Connects navigation signals to the index switch methods
        self.signin_page.switch_to_Register.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.register_page.switch_to_SignIn.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        # Connect theme toggles for both pages
        self.signin_page.toggle_btn.clicked.connect(self.toggle_theme)
        self.register_page.toggle_btn.clicked.connect(self.toggle_theme)

        self.apply_theme()

    def toggle_theme(self):
        # Switches the theme state and re-applies the corresponding QSS file to the app.
        self.is_dark_mode = not self.is_dark_mode
        # Sets the theme for all pages in the stack.
        theme_text = "☀️ Light Mode" if self.is_dark_mode else "🌑 Dark Mode"
        self.signin_page.toggle_btn.setText(theme_text)
        self.register_page.toggle_btn.setText(theme_text)
        self.apply_theme()

    # Sets filename to the chosen theme, enables toggle to dark as initial theme is light.
    def apply_theme(self):
        filename = "dark.qss" if self.is_dark_mode else "light.qss"
        filepath = f"styles/{filename}"
        with open(filepath, "r") as file:
            self.setStyleSheet(file.read())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())