import json
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QComboBox, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from datetime import date
from PySide6.QtCore import Qt, Signal
from pages.base_page import BasePage
from pages.todos.task_modal import TaskModal
from helpers import read_json, write_json

TASKS_FILE = "assets/mock_data/tasks.json"

class PersonalTodoPage(BasePage):
    to_Todo = Signal()

    def __init__(self, current_user = None):
        super().__init__()
        self.current_user = current_user
        self.load_tasks()
        self.populate_content()

    def showEvent(self, event):
        # Grabs current user from Main Window on page load.
        super().showEvent(event)
        main_window = self.window()
        if hasattr(main_window, "current_user"):
            self.current_user = main_window.current_user
        self.load_tasks()
        self.populate_content()

    def get_current_user_name(self) -> str:
        if self.current_user and hasattr(self.current_user, "name"):
            return self.current_user.name
        return ""

    def define_widgets(self) -> None:
        self.title = QLabel("☑️ Personal To-Do List")
        self.title.setObjectName("HeadingLabel")
        
        self.add_btn = QPushButton("+ Add Personal Task")
        self.add_btn.setObjectName("LoginButton")
        self.add_btn.clicked.connect(self.add_personal_modal)

        self.back_btn = QPushButton("◀️ To to-do menu")
        self.back_btn.setObjectName("NavButton")
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setFixedWidth(300)
        self.back_btn.clicked.connect(self.to_Todo.emit)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Task Name", "Status", "Assigned Date", "Due Date", "Details", "Actions"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 5):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        self.table.verticalHeader().setVisible(False)

    def assemble_widgets(self) -> None:
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.back_btn)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.table)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def load_tasks(self):
        try:
            self.tasks = read_json(TASKS_FILE)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def populate_content(self):
        current_user_name = self.get_current_user_name()

        # Only gives tasks that belong to current user.
        self.personal_tasks = [
            t for t in self.tasks 
            if t.get("type") == "personal" and t.get("owner") == current_user_name
        ]

        # Pushes Complete and Suspended tasks to bottom of stack.
        def sort_key(task):
            status = task.get("status", "").lower()
            if "complete" in status or "suspended" in status:
                return (1, task.get("task_name", ""))
            return (0, task.get("task_name", ""))
        self.personal_tasks.sort(key = sort_key)
        
        self.table.setRowCount(len(self.personal_tasks))
        for row_index, task in enumerate(self.personal_tasks):
            self.table.setItem(row_index, 0, QTableWidgetItem(task.get("task_name", "")))

            # Dropdown menu for task status.
            status_combo = QComboBox()
            status_combo.addItems(["⏳ In Progress", "💬 Awaiting Info", "✅ Complete", "❌ Suspended"])
            current_status = task.get("status", "⏳ In Progress")
            if current_status in ["⏳ In Progress", "💬 Awaiting Info", "✅ Complete", "❌ Suspended"]:
                status_combo.setCurrentText(current_status)
            else:
                status_combo.setCurrentText("In Progress")
            status_combo.currentTextChanged.connect(lambda new_status, t = task: self.handle_status_change(t, new_status))
            self.table.setCellWidget(row_index, 1, status_combo)

            self.table.setItem(row_index, 2, QTableWidgetItem(task.get("assigned_date", "")))
            self.table.setItem(row_index, 3, QTableWidgetItem(task.get("due_date", "")))

            # View/Edit task buttons.
            details_btn = QPushButton("More Details")
            details_btn.setObjectName("NavButton")
            details_btn.clicked.connect(lambda checked = False, t = task: self.show_details(t))
            self.table.setCellWidget(row_index, 4, details_btn)

            action_btn = QPushButton("Edit/Delete")
            action_btn.setObjectName("NavButton")
            action_btn.clicked.connect(lambda checked = False, t = task: self.show_modal(t))
            self.table.setCellWidget(row_index, 5, action_btn)

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
            write_json(TASKS_FILE, self.tasks)
            self.load_tasks()
            self.populate_content()
        elif dialog.action_result == "delete":
            confirm = QMessageBox.question(self, "Confirm Delete", 
                f"Are you sure you want to delete '{task.get('task_name', 'Task')}'?",
                QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                if task in self.tasks:
                    self.tasks.remove(task)
                    write_json(TASKS_FILE, self.tasks)
                    self.load_tasks()
                    self.populate_content()

    def handle_status_change(self, task, new_status):
        # Updates new status in JSON.
        task["status"] = new_status
        write_json(TASKS_FILE, self.tasks)
        self.populate_content()

    def add_personal_modal(self):
        current_user_name = self.get_current_user_name()

        new_task = {
            "task_name": "",
            "status": "⏳ In Progress",
            "assigned_date": "",
            "due_date": date.today().isoformat(),
            "details": "",
            "type": "personal",
            "owner": current_user_name
        }

        dialog = TaskModal(new_task, self)
        dialog.exec()

        if dialog.action_result == "save":
            if not new_task.get("task_name", "").strip():
                QMessageBox.warning(self, "❌ Error", "Task name field cannot be empty.")
                return
            
            self.tasks.append(new_task)
            write_json(TASKS_FILE, self.tasks)
            self.load_tasks()
            self.populate_content()