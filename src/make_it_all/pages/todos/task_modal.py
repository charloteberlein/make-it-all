import os
import re
import shutil
from datetime import date

from PySide6.QtCore import QDate
from PySide6.QtGui import QFont, QTextCharFormat
from PySide6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)

from make_it_all.helpers import ASSETS_DIR
from make_it_all.pages.todos.task_status import TaskStatus, parse_task_status


class TaskModal(QDialog):
    """A clean popup modal for viewing/editing task details."""

    def __init__(self, task_dict: dict, parent=None):
        super().__init__(parent)
        self.task_dict = task_dict
        self.action_result = None

        task_name = task_dict.get("task_name")
        self.setWindowTitle(f"Task Details: {task_name}")
        self.resize(650, 500)

        self.form_layout = QFormLayout(self)
        self.form_layout.setContentsMargins(50, 60, 50, 60)

        self.name_input = QLineEdit(task_name)
        self.status_input = QLabel(parse_task_status(task_dict.get("status", "")).value)
        # Sets default task creation status.
        if not task_name:
            self.status_input.setText(TaskStatus.IN_PROGRESS.value)

        self.is_project = task_dict.get("type") == "project"
        if self.is_project:
            self.project_input = QLineEdit(task_dict.get("project_name", ""))
            self.assigner_input = QLineEdit(task_dict.get("assigner", ""))
            self.assignees_input = QLineEdit(task_dict.get("assignees", ""))

            # Adds estimate hours spent counter, increments of 0.25 => easy to convert to hours.
            self.estimated_input = QDoubleSpinBox()
            self.estimated_input.setRange(0.0, 9999.0)
            self.estimated_input.setSingleStep(0.25)
            try:
                self.estimated_input.setValue(float(task_dict.get("estimated_time", 0.0)))
            except (ValueError, TypeError):
                self.estimated_input.setValue(0.0)

        # Adds calander for date select.
        self.due_input = QDateEdit()
        self.due_input.setCalendarPopup(True)
        due_str = task_dict.get("due_date", "")
        if due_str:
            date_val = QDate.fromString(due_str, "yyyy-MM-dd")
            if date_val.isValid():
                self.due_input.setDate(date_val)
            else:
                self.due_input.setDate(QDate.currentDate())
        else:
            self.due_input.setDate(QDate.currentDate())

        # Allows for images to be added.
        self.details_editor = QTextEdit()
        raw_details = task_dict.get("details", "")
        if raw_details:
            converted_details = re.sub(
                r"!\[([^\]]*)\]\(([^)]+)\)",
                r'<img src="\2" width="300" style="max-width:100%;"/>',
                raw_details,
            )
            self.details_editor.setMarkdown(converted_details)
        else:
            self.details_editor.setMarkdown("")
        self.details_editor.setPlaceholderText(
            "Type notes, insert code snippets, links, or images here..."
        )

        self.form_layout.addRow("Task Name:", self.name_input)

        if self.is_project:
            self.form_layout.addRow("Project Name:", self.project_input)
            self.form_layout.addRow("Assigner:", self.assigner_input)
            self.form_layout.addRow("Assignees:", self.assignees_input)
            self.form_layout.addRow("Estimated Time (Hours):", self.estimated_input)
        self.form_layout.addRow("Status:", self.status_input)
        self.form_layout.addRow("Due Date:", self.due_input)
        self.form_layout.addRow("Rich Notes/Code:", self.details_editor)

        # Rich formatting options.
        actions_layout = QHBoxLayout()
        bold_btn = QPushButton("Bold")
        bold_btn.setCheckable(True)
        bold_btn.clicked.connect(
            lambda checked: self.details_editor.setFontWeight(
                QFont.Weight.Bold if checked else QFont.Weight.Normal
            )
        )

        code_btn = QPushButton("💻 Code")
        code_btn.setCheckable(True)
        code_btn.clicked.connect(self.apply_code)

        image_btn = QPushButton("🖼️ Image")
        image_btn.clicked.connect(self.insert_image)

        actions_layout.addWidget(bold_btn)
        actions_layout.addWidget(code_btn)
        actions_layout.addWidget(image_btn)
        actions_layout.addStretch()
        self.form_layout.addRow("", actions_layout)

        bottom_layout = QHBoxLayout()

        self.delete_btn = QPushButton("Delete Task")
        self.delete_btn.setObjectName("NavButton")
        self.delete_btn.clicked.connect(self.on_delete)
        bottom_layout.addWidget(self.delete_btn)

        bottom_layout.addStretch()

        save_cancel_layout = QHBoxLayout()
        save_cancel_layout.setSpacing(16)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("NavButton")
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("NavButton")
        self.save_btn.clicked.connect(self.accept_edits)

        save_cancel_layout.addWidget(self.cancel_btn)
        save_cancel_layout.addWidget(self.save_btn)

        bottom_layout.addLayout(save_cancel_layout)

        self.form_layout.addRow(bottom_layout)

    def apply_code(self):
        cursor = self.details_editor.textCursor()
        format = QTextCharFormat()

        font_family = "Consolas" if os.name == "nt" else "Monospace"
        code_font = QFont(font_family, 10, QFont.Weight.Normal)
        format.setFont(code_font)

        cursor.mergeCharFormat(format)
        self.details_editor.mergeCurrentCharFormat(format)

        if not cursor.hasSelection():
            cursor.insertText("code_snippet")

    def insert_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images: (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            image_directory = ASSETS_DIR / "task_images"
            image_directory.mkdir(parents=True, exist_ok=True)
            filename = os.path.basename(file_path)
            destination_path = image_directory / filename

            shutil.copy(file_path, destination_path)

            # Inserts HTML img tag -> enables image rendering in modal.
            html_img = (
                f'<br><img src="{destination_path.as_posix()}" width="300" '
                'style="max-width:100%;"/><br>'
            )
            self.details_editor.textCursor().insertHtml(html_img)

    # Create task structure.
    def accept_edits(self):
        self.task_dict["task_name"] = self.name_input.text()
        new_status = parse_task_status(self.status_input.text())
        self.task_dict["status"] = new_status.value
        if self.is_project:
            self.task_dict["project_name"] = self.project_input.text()
            self.task_dict["assigner"] = self.assigner_input.text()
            self.task_dict["assignees"] = self.assignees_input.text()

            if new_status is TaskStatus.COMPLETED:
                if not self.task_dict.get("completion_date"):
                    self.task_dict["completion_date"] = date.today().isoformat()
            else:
                self.task_dict["completion_date"] = ""

        if self.is_project:
            self.task_dict["estimated_time"] = str(self.estimated_input.value())
        self.task_dict["due_date"] = self.due_input.date().toString("yyyy-MM-dd")
        self.task_dict["details"] = self.details_editor.toMarkdown()
        self.action_result = "save"
        self.accept()

    def on_delete(self):
        self.action_result = "delete"
        self.reject()
