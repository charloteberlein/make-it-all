from datetime import date

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
)

from make_it_all.data.tasks import load_tasks, save_tasks
from make_it_all.pages.base_page import BasePage
from make_it_all.pages.todos.task_modal import TaskModal
from make_it_all.pages.todos.task_status import TaskStatus, parse_task_status, task_status_options


class PersonalTodoPage(BasePage):
    to_Todo = Signal()

    def __init__(self, current_user=None):
        super().__init__()
        self.current_user = current_user
        if self.current_user:
            self.load_tasks()
            self.populate_content()

    def showEvent(self, event):
        """Grabs current user from Main Window on page load."""
        super().showEvent(event)
        self.current_user = getattr(self.window(), "current_user", None)
        self.load_tasks()
        self.populate_content()

    def get_current_user_name(self) -> str:
        if self.current_user and hasattr(self.current_user, "name"):
            return self.current_user.name
        return ""

    def define_widgets(self) -> None:
        self.title = QLabel("☑️ Personal To-do List")
        self.title.setObjectName("HeadingLabel")

        self.add_btn = QPushButton("+ Add Personal Task")
        self.add_btn.setObjectName("LoginButton")
        self.add_btn.clicked.connect(self.add_personal_modal)

        self.back_btn = QPushButton("◀️ To to-do menu")
        self.back_btn.setObjectName("NavButton")
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setFixedWidth(300)
        self.back_btn.clicked.connect(self.to_Todo.emit)

        self.no_tasks_label = QLabel("You have no current personal tasks")
        self.no_tasks_label.setObjectName("SubHeadingLabel")
        self.no_tasks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_tasks_label.setVisible(False)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Task Name", "Status", "Due Date", "Details", "Actions"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.table.verticalHeader().setVisible(False)

    def assemble_widgets(self) -> None:
        self.page_layout.addWidget(self.title)
        self.page_layout.addSpacing(20)
        self.page_layout.addWidget(self.back_btn)
        self.page_layout.addSpacing(20)
        self.page_layout.addWidget(self.add_btn)
        self.page_layout.addWidget(self.no_tasks_label)
        self.page_layout.addSpacing(10)
        self.page_layout.addWidget(self.table)
        self.page_layout.addStretch()
        self.setLayout(self.page_layout)

    def load_tasks(self):
        self.tasks = load_tasks()

    def populate_content(self):
        current_user_name = self.get_current_user_name()

        # Only gives tasks that belong to current user.
        self.personal_tasks = [
            t
            for t in self.tasks
            if t.get("type") == "personal" and t.get("owner") == current_user_name
        ]

        if not self.personal_tasks:
            self.table.setVisible(False)
            self.no_tasks_label.setVisible(True)
            return

        self.table.setVisible(True)
        self.no_tasks_label.setVisible(False)

        # Pushes Complete and Suspended tasks to bottom of stack.
        def sort_key(task):
            status = parse_task_status(task.get("status", ""))
            if status in (TaskStatus.COMPLETED, TaskStatus.SUSPENDED):
                return (1, task.get("task_name", ""))
            return (0, task.get("task_name", ""))

        self.personal_tasks.sort(key=sort_key)

        self.table.setRowCount(len(self.personal_tasks))
        for row_index, task in enumerate(self.personal_tasks):
            self.table.setItem(row_index, 0, QTableWidgetItem(task.get("task_name", "")))

            # Dropdown menu for task status.
            status_combo = QComboBox()
            status_combo.setObjectName("TableStatusCombo")
            status_combo.addItems(task_status_options())
            current_status = parse_task_status(task.get("status", ""))
            status_combo.setCurrentText(current_status.value)
            status_combo.currentTextChanged.connect(
                lambda new_status, t=task: self.handle_status_change(t, new_status)
            )
            self.table.setCellWidget(row_index, 1, status_combo)

            self.table.setItem(row_index, 2, QTableWidgetItem(task.get("due_date", "")))

            # View/Edit task buttons.
            details_btn = QPushButton("More Details")
            details_btn.setObjectName("EditNavButton")
            details_btn.clicked.connect(lambda checked=False, t=task: self.show_details(t))
            self.table.setCellWidget(row_index, 3, details_btn)

            action_btn = QPushButton("Edit/Delete")
            action_btn.setObjectName("EditNavButton")
            action_btn.clicked.connect(lambda checked=False, t=task: self.show_modal(t))
            self.table.setCellWidget(row_index, 4, action_btn)

    def show_details(self, task):
        # Creates a dialog box to allow for read-only rich formatting.
        task_name = task.get("task_name", "Task")
        details = task.get("details", "No details provided.")

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Details: {task_name}")
        dialog.resize(500, 400)

        layout = QVBoxLayout(dialog)
        editor = QTextEdit()
        editor.setReadOnly(True)
        editor.setMarkdown(details)
        layout.addWidget(editor)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("LoginButton")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        dialog.exec()

    def show_modal(self, task):
        # To edit task.
        dialog = TaskModal(task, self)
        dialog.exec()

        if dialog.action_result == "save":
            save_tasks(self.tasks)
            self.load_tasks()
            self.populate_content()
        elif dialog.action_result == "delete":
            confirm = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete '{task.get('task_name', 'Task')}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if confirm == QMessageBox.StandardButton.Yes and task in self.tasks:
                self.tasks.remove(task)
                save_tasks(self.tasks)
                self.load_tasks()
                self.populate_content()

    def handle_status_change(self, task, new_status):
        # Update the task status.
        task["status"] = parse_task_status(new_status).value
        save_tasks(self.tasks)
        self.populate_content()

    def add_personal_modal(self):
        current_user_name = self.get_current_user_name()
        # Add a new personal task.
        new_task = {
            "task_name": "",
            "status": TaskStatus.IN_PROGRESS.value,
            "assigned_date": "",
            "due_date": date.today().isoformat(),
            "details": "",
            "type": "personal",
            "owner": current_user_name,
        }

        dialog = TaskModal(new_task, self)
        dialog.exec()

        if dialog.action_result == "save":
            if not new_task.get("task_name", "").strip():
                QMessageBox.warning(self, "❌ Error", "Task name field cannot be empty.")
                return

            self.tasks.append(new_task)
            save_tasks(self.tasks)
            self.load_tasks()
            self.populate_content()
