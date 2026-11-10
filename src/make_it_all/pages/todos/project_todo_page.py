from datetime import date

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
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


class ProjectTodoPage(BasePage):
    to_Todo = Signal()

    def __init__(self, current_user = None):
        super().__init__()
        self.current_user = current_user
        self.load_tasks()
        self.populate_content()

    def showEvent(self, event):
        """ Grabs current user from Main Window on page load. """
        super().showEvent(event)
        main_window = self.window()
        if hasattr(main_window, "current_user"):
            self.current_user = main_window.current_user
        self.load_tasks()
        self.populate_content()
        self.update_permissions()

    def get_current_user(self) -> str:
            if self.current_user and hasattr(self.current_user, "name"):
                return self.current_user.name
            return ""

    def add_task(self) -> bool:
        # Checks user's rank for project task creation.
        user = getattr(self, "current_user", None)
        if not user or not hasattr(user, "rank"):
            return False
        rank = str(user.rank).strip().lower()
        return rank in ["manager", "team lead"]

    def update_permissions(self):
        if hasattr(self, "add_btn"):
            self.add_btn.setVisible(self.add_task()) # Only Team Leaders/Managers can access make task button.

    def define_widgets(self) -> None:
        self.title = QLabel("📋 Project To-do List")
        self.title.setObjectName("HeadingLabel")

        self.add_btn = QPushButton("+ Add Project Task")
        self.add_btn.setObjectName("LoginButton")
        self.add_btn.clicked.connect(self.add_project_modal)

        self.back_btn = QPushButton("◀️ To to-do menu")
        self.back_btn.setObjectName("NavButton")
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setFixedWidth(300)
        self.back_btn.clicked.connect(self.to_Todo.emit)

        self.no_tasks_label = QLabel("You have no current project tasks.")
        self.no_tasks_label.setObjectName("SubHeadingLabel")
        self.no_tasks_label.setAlignment(Qt.AlignCenter)
        self.no_tasks_label.setVisible(False)

        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "Task Name", "Project Name", "Assigner", "Assignees", "Status", "Assigned Date",
            "Due Date", "Estimated Hours", "Actual Hours", "More Info", "Actions"
        ])
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        self.table.setColumnWidth(0, 210)
        for i in range(1, 11):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setAutoScroll(True)

    def assemble_widgets(self) -> None:
        self.layout.addWidget(self.title)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.back_btn)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.add_btn)
        self.layout.addSpacing(14)
        self.layout.addWidget(self.no_tasks_label)
        self.layout.addWidget(self.table)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def load_tasks(self):
        self.tasks = load_tasks()

    def populate_content(self):
        self.project_tasks = [t for t in self.tasks if t.get("type", "project") == "project"]

        if not self.project_tasks:
            self.table.setVisible(False)
            self.no_tasks_label.setVisible(True)
            return

        self.table.setVisible(True)
        self.no_tasks_label.setVisible(False)

        # Pushes Completed and Suspended tasks to bottom of stack.
        def sort_key(task):
            status = parse_task_status(task.get("status"))
            if status in (TaskStatus.COMPLETED, TaskStatus.SUSPENDED):
                return (1, task.get("task_name", ""))
            return (0, task.get("task_name", ""))
        self.project_tasks.sort(key = sort_key)
        
        self.table.setRowCount(len(self.project_tasks))
        for row_index, task in enumerate(self.project_tasks):
            self.table.setItem(row_index, 0, QTableWidgetItem(task.get("task_name", "")))
            self.table.setItem(row_index, 1, QTableWidgetItem(task.get("project_name", "")))
            self.table.setItem(row_index, 2, QTableWidgetItem(task.get("assigner", "")))
            
            assignees_data = task.get("assignees", "")
            assignees_str = ", ".join(assignees_data) if isinstance(assignees_data, list) else str(assignees_data)
            self.table.setItem(row_index, 3, QTableWidgetItem(assignees_str))

            # Dropdownm menu.
            status_combo = QComboBox()
            status_combo.setObjectName("TableStatusCombo")
            status_combo.addItems(task_status_options())
            current_status = parse_task_status(task.get("status"))
            status_combo.setCurrentText(current_status.value)
            status_combo.currentTextChanged.connect(
                lambda new_status, t = task, combo = status_combo:
                self.handle_status_change(t, new_status, combo)
            )
            self.table.setCellWidget(row_index, 4, status_combo)
            
            self.table.setItem(row_index, 5, QTableWidgetItem(task.get("assigned_date", "")))
            self.table.setItem(row_index, 6, QTableWidgetItem(task.get("due_date", "")))

            est_time = task.get("estimated_time", "0.0")
            self.table.setItem(row_index, 7, QTableWidgetItem(str(est_time)))

            # Actual time spent counter.
            actual_spin = QDoubleSpinBox()
            actual_spin.setRange(0.0, 9999.0)
            actual_spin.setSingleStep(0.5)
            try:
                actual_spin.setValue(float(task.get("actual_time", 0.0)))
            except (ValueError, TypeError):
                actual_spin.setValue(0.0)

            actual_spin.valueChanged.connect(lambda val, t=task: self.handle_actual_time(t, val))
            self.table.setCellWidget(row_index, 8, actual_spin)

            # View/Edit Modal Buttons.
            details_btn = QPushButton("More Details")
            details_btn.setObjectName("EditNavButton")
            details_btn.clicked.connect(lambda checked = False, t = task: self.check_and_show_details(t))
            self.table.setCellWidget(row_index, 9, details_btn)

            action_btn = QPushButton("Edit/Delete")
            action_btn.setObjectName("EditNavButton")
            action_btn.clicked.connect(lambda checked = False, t = task: self.show_modal(t))
            self.table.setCellWidget(row_index, 10, action_btn)

    def check_and_show_details(self, task):
        current_user_name = self.get_current_user()
        assigner = task.get("assigner", "")
        assignees = task.get("assignees", "")

        # Enforces data protection, only those assigning/assigned to task can see more details.
        if isinstance(assignees, list):
            assignee_list = [a.strip() for a in assignees]
        else:
            assignee_list = [a.strip() for a in str(assignees).split(",")]
        is_assigner = current_user_name == assigner
        is_assignee = current_user_name in assignee_list
        if is_assigner or is_assignee:
            task_name = task.get("task_name", "Task")
            details = task.get("details", "No details provided.")

            # Creates a dialog box to allow for read-only rich formatting.
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Details: {task_name}")
            dialog.resize(400, 400)
            
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

        else:
            QMessageBox.warning(self, "❌ Access Denied", "You cannot view this task's details, as you are not assigned to it.")

    def show_modal(self, task):
        current_user_name = self.get_current_user()
        assigner = task.get("assigner", "")
        assignees = task.get("assignees", "")

        if isinstance(assignees, list):
            assignee_list = [a.strip() for a in assignees]
        else:
            assignee_list = [a.strip() for a in str(assignees).split(",")]

        is_assigner = current_user_name == assigner
        is_assignee = current_user_name in assignee_list

        if not (is_assigner or is_assignee):
            QMessageBox.warning(self, "❌ Access Denied", "You cannot edit or delete this task as you are not assigned to it.")
            return
        
        dialog = TaskModal(task, self)
        dialog.exec()

        if dialog.action_result == "save":
            save_tasks(self.tasks)
            self.load_tasks()
            self.populate_content()
        elif dialog.action_result == "delete":
            confirm = QMessageBox.question(self, "Confirm Delete", 
                f"Are you sure you want to delete '{task.get('task_name', 'Task')}'?",
                QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                if task in self.tasks:
                    self.tasks.remove(task)
                    save_tasks(self.tasks)
                    self.load_tasks()
                    self.populate_content()

    def handle_status_change(self, task, new_status, combo_box):
        # Validates current user == assigner/assignee before changing task status.
        current_user_name = self.get_current_user()
        assigner = task.get("assigner", "")
        assignees = task.get("assignees", "")

        if isinstance(assignees, list):
            assignee_list = [a.strip() for a in assignees]
        else:
            assignee_list = [a.strip() for a in str(assignees).split(",")]

        is_assigner = current_user_name == assigner
        is_assignee = current_user_name in assignee_list

        # Another data protection measure, POLP.
        if not (is_assigner or is_assignee):
            QMessageBox.warning(self, "❌ Access Denied", "You can only change the status of tasks you are assigned to.")
            combo_box.blockSignals(True)
            combo_box.setCurrentText(parse_task_status(task.get("status")).value)
            combo_box.blockSignals(False)
            return

        # Task completion tracking.
        task_status = parse_task_status(new_status)
        task["status"] = task_status.value
        if task_status is TaskStatus.COMPLETED:
            if not task.get("completion_date"):
                task["completion_date"] = date.today().isoformat()
        else:
            task["completion_date"] = ""

        save_tasks(self.tasks)
        self.load_tasks()
        self.populate_content()

    def handle_actual_time(self, task, value):
        task["actual_time"] = str(value)
        save_tasks(self.tasks)

    def add_project_modal(self):
        current_user_name = self.get_current_user()
        # Create a new project task.
        new_project_task = {
            "task_name": "",
            "project_name": "",
            "assigner": current_user_name,
            "assignees": "",
            "status": TaskStatus.IN_PROGRESS.value,
            "assigned_date": date.today().isoformat(),
            "due_date": "",
            "estimated_time": "",
            "actual_time": "0.0" ,
            "details": "",
            "type": "project",
            "completion_date": ""
        }

        dialog = TaskModal(new_project_task, self)
        dialog.exec()

        if dialog.action_result == "save":
            if not new_project_task.get("task_name", "").strip():
                QMessageBox.warning(self, "❌ Error", "Task name field cannot be empty.")
                return
            
            self.tasks.append(new_project_task)
            save_tasks(self.tasks)
            self.load_tasks()
            self.populate_content()