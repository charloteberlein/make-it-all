import json
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel, QDialog, QFrame, QVBoxLayout, QHBoxLayout, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QWidget
)
from PySide6.QtCharts import QBarCategoryAxis, QBarSeries, QBarSet, QChart, QChartView, QValueAxis # type: ignore

from pages.base_page import BasePage
from helpers import read_json
from pages.todos.task_analytics import (
    calc_project_completion_percentages, calc_project_task_status_counts,
    calc_employee_task_status_counts, get_emp_tasks, calc_project_hours, calc_emp_hours_summary
)
from pages.todos.task_status import TaskStatus

TASKS_FILE = "assets/mock_data/tasks.json"


class ClickableChartView(QChartView):
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class DashboardPage(BasePage):
    to_Training = Signal()

    def __init__(self, current_user=None):
        self.current_user = current_user
        super().__init__()
        self.load_tasks()
        self.populate_content()

    def showEvent(self, event):
        super().showEvent(event)
        main_window = self.window()
        if hasattr(main_window, "current_user") and main_window.current_user:
            self.current_user = main_window.current_user
        self.training_btn.setVisible(
            bool(self.current_user and self.current_user.rank in ["Manager", "Team Lead"])
        )
        self.load_tasks()
        self.populate_content()

    def get_current_user_name(self) -> str:
        if self.current_user and hasattr(self.current_user, "name"):
            return self.current_user.name
        return ""

    def define_layout(self) -> None:
        super().define_layout()

        self.training_btn = QPushButton("▶️ To Training Page")
        self.training_btn.setObjectName("NavButton")
        self.training_btn.setCursor(Qt.PointingHandCursor)
        self.training_btn.setFixedWidth(200)
        self.training_btn.clicked.connect(self.to_Training.emit)

        self.progress_frame = QFrame()
        self.progress_frame.setObjectName("ProgFrame")
        self.progress_layout = QVBoxLayout(self.progress_frame)

        self.title_frame = QFrame()
        self.title_layout = QHBoxLayout(self.title_frame)

        self.chart_layout = QHBoxLayout()
        self.chart_layout.setSpacing(14)

        self.hours_chart_layout = QHBoxLayout()
        self.hours_chart_layout.setSpacing(14)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(14)
        self.scroll_content.setLayout(self.scroll_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setWidget(self.scroll_content)

    def define_widgets(self) -> None:
        self.title_label = QLabel("Dashboard")
        self.title_label.setObjectName("HeadingLabel")

        self.progress_tracker_header = QLabel("My Project Progress")
        self.progress_tracker_header.setObjectName("SubheadingLabel")
        self.progress_tracker_header.setContentsMargins(9, 0, 9, 0)

        self.hours_section_header = QLabel("Hours & Workload Overview")
        self.hours_section_header.setObjectName("SubheadingLabel")
        self.hours_section_header.setContentsMargins(9, 0, 9, 0)

        self.training_btn = QPushButton("▶️ To Training Page")
        self.training_btn.setObjectName("NavButton")
        self.training_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.training_btn.setFixedWidth(200)
        self.training_btn.clicked.connect(self.to_Training.emit)

        self.chart_section_header = QLabel("Task Status Overview")
        self.chart_section_header.setObjectName("SubheadingLabel")
        self.chart_section_header.setContentsMargins(9, 0, 9, 0)

    def assemble_widgets(self) -> None:
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.training_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.scroll_layout.addWidget(self.title_frame)
        self.scroll_layout.addWidget(self.progress_tracker_header)
        self.scroll_layout.addWidget(self.progress_frame)
        self.scroll_layout.addWidget(self.chart_section_header)
        self.scroll_layout.addLayout(self.chart_layout)
        self.scroll_layout.addWidget(self.hours_section_header)
        self.scroll_layout.addLayout(self.hours_chart_layout)
        self.scroll_layout.addStretch(1)

        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)

    def load_tasks(self):
        try:
            self.tasks = read_json(TASKS_FILE)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def populate_content(self):
        while self.progress_layout.count():
            item = self.progress_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        while self.chart_layout.count():
            item = self.chart_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        while self.hours_chart_layout.count():
            item = self.hours_chart_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        user_name = self.get_current_user_name()
        if user_name:
            self.title_label.setText(f"{user_name}'s Dashboard")
        else:
            self.title_label.setText("Dashboard")

        all_percentages = calc_project_completion_percentages(TASKS_FILE)
        emp_data = get_emp_tasks(TASKS_FILE)
        user_projects = set()

        if user_name in emp_data:
            user_tasks = emp_data[user_name]["completed"] + emp_data[user_name]["active"]
            for task in user_tasks:
                project_name = task.get("project_name", "General").strip()
                if project_name:
                    user_projects.add(project_name)

        for task in self.tasks:
            if task.get("type") == "project":
                assigner = str(task.get("assigner", "")).strip()
                if user_name and assigner.lower() == user_name.lower():
                    project_name = task.get("project_name", "General").strip()
                    if project_name:
                        user_projects.add(project_name)

        if not user_name:
            filtered_stats = all_percentages
        else:
            filtered_stats = {
                project: data
                for project, data in all_percentages.items()
                if project in user_projects
            }

        if not filtered_stats:
            self.progress_layout.addWidget(
                QLabel("You are currently not assigned to any active projects.")
            )
        else:
            for project_name, data in filtered_stats.items():
                total = data["total"]
                completed = data["completed"]
                percent = data["percentage"]
                self.progress_layout.addWidget(
                    QLabel(f"{project_name} — {percent}% ({completed}/{total} completed)")
                )

                bar = QProgressBar()
                bar.setObjectName("ProjectProgressBar")
                bar.setValue(int(percent))
                bar.setFixedHeight(18)
                bar.setTextVisible(False)
                self.progress_layout.addWidget(bar)
                self.progress_layout.addSpacing(14)

        is_employee = self.current_user and self.current_user.rank == "Employee"
        self.chart_layout.addWidget(
            self._create_status_chart(
                "Tasks by Project",
                calc_project_task_status_counts(TASKS_FILE, user_name if is_employee else None),
            ), 1,
        )
        self.chart_layout.addWidget(
            self._create_status_chart(
                "Tasks by Employee",
                calc_employee_task_status_counts(TASKS_FILE, user_name if is_employee else None),
            ), 1,
        )

        self.hours_chart_layout.addWidget(
            self._create_project_efficiency_chart(clickable=True, filter_user=user_name if is_employee else None), 1
        )
        self.hours_chart_layout.addWidget(
            self._create_employee_hours_chart(clickable=True, filter_user=user_name if is_employee else None), 1
        )

    def _create_status_chart(self, title, grouped_counts, clickable=True):
        chart = QChart()

        # Get light/dark mode from main window attributes
        main_window = self.window()
        is_dark_mode = bool(getattr(main_window, "is_dark_mode", False))
        chart.setTheme(
            QChart.ChartTheme.ChartThemeDark
            if is_dark_mode
            else QChart.ChartTheme.ChartThemeLight
        )

        chart.setTitle(title)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        # Data series
        series = QBarSeries()
        chart_statuses = (
            (TaskStatus.AWAITING_INFO, "Awaiting Info"),
            (TaskStatus.IN_PROGRESS, "In Progress"),
            (TaskStatus.COMPLETED, "Completed"),
        )
        for status, label in chart_statuses:
            bar_set = QBarSet(label)
            if status is TaskStatus.AWAITING_INFO:
                bar_set.setColor("#A5BDF1")
            elif status is TaskStatus.IN_PROGRESS:
                bar_set.setColor("#CA8A04")
            else:
                bar_set.setColor("#13AC53")
            values = [counts[status] for counts in grouped_counts.values()]
            bar_set.append(values or [0])
            series.append(bar_set)
        chart.addSeries(series)

        categories = list(grouped_counts)
        category_axis = QBarCategoryAxis()
        category_axis.append(categories or ["No tasks."])

        # Define axes
        value_axis = QValueAxis()
        max_count = max(
            count for counts in grouped_counts.values() for count in counts.values()
        ) if len(grouped_counts) > 0 else 0
        value_axis.setRange(0, max(1, max_count))
        value_axis.setLabelFormat("%d")

        chart.addAxis(category_axis, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(category_axis)
        series.attachAxis(value_axis)

        if clickable:
            chart_view = ClickableChartView(chart)
            chart_view.clicked.connect(lambda t=title, gc=grouped_counts: self.chart_modal(t, gc))
        else:
            chart_view = QChartView(chart)

        chart_view.setObjectName("DashboardChartView")
        chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        chart_view.setMinimumWidth(0)
        chart_view.setMinimumHeight(250)

        return chart_view

    def _create_project_efficiency_chart(self, clickable=True, filter_user=None):
        data = calc_project_hours(TASKS_FILE)
        project_details = data.get("details", {})

        if filter_user:
            emp_data = get_emp_tasks(TASKS_FILE)
            user_projects = set()
            if filter_user in emp_data:
                user_tasks = emp_data[filter_user]["completed"] + emp_data[filter_user]["active"]
                for task in user_tasks:
                    proj = task.get("project_name", "General").strip()
                    if proj:
                        user_projects.add(proj)
            project_details = {p: m for p, m in project_details.items() if p in user_projects}

        chart = QChart()
        main_window = self.window()
        is_dark_mode = bool(getattr(main_window, "is_dark_mode", False))
        chart.setTheme(QChart.ChartTheme.ChartThemeDark if is_dark_mode else QChart.ChartTheme.ChartThemeLight)
        chart.setTitle("Project Efficiency (Estimated vs Actual Hours)")
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        series = QBarSeries()
        est_set = QBarSet("Estimated Hours")
        est_set.setColor("#AF22EB")
        act_set = QBarSet("Actual Hours")
        act_set.setColor("#2290EB")

        categories = list(project_details.keys())
        est_values, act_values = [], []
        for proj_name, metrics in project_details.items():
            est_values.append(metrics["total_estimated"])
            act_values.append(metrics["total_actual"])

        est_set.append(est_values or [0])
        act_set.append(act_values or [0])
        series.append(est_set)
        series.append(act_set)
        chart.addSeries(series)

        category_axis = QBarCategoryAxis()
        category_axis.append(categories or ["No projects."])

        value_axis = QValueAxis()
        max_val = max(est_values + act_values) if (est_values and act_values) else 10
        value_axis.setRange(0, max(1, int(max_val * 1.1)))
        value_axis.setLabelFormat("%d")

        chart.addAxis(category_axis, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(category_axis)
        series.attachAxis(value_axis)

        if clickable:
            chart_view = ClickableChartView(chart)
            chart_view.clicked.connect(lambda fuser=filter_user: self.hours_chart_modal("Project Efficiency (Estimated vs Actual Time Spent)", self._create_project_efficiency_chart, fuser))
        else:
            chart_view = QChartView(chart)

        chart_view.setObjectName("DashboardChartView")
        chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        chart_view.setMinimumWidth(0)
        chart_view.setMinimumHeight(250)

        return chart_view

    def _create_employee_hours_chart(self, clickable=True, filter_user=None):
        emp_data = calc_emp_hours_summary(TASKS_FILE)

        if filter_user:
            emp_data = {emp: metrics for emp, metrics in emp_data.items() if emp.lower() == filter_user.lower()}

        chart = QChart()
        main_window = self.window()
        is_dark_mode = bool(getattr(main_window, "is_dark_mode", False))
        chart.setTheme(QChart.ChartTheme.ChartThemeDark if is_dark_mode else QChart.ChartTheme.ChartThemeLight)
        chart_title = "My Workload & Hours" if filter_user else "Individual Employee Workload (Estimated vs Actual Hours)"
        chart.setTitle(chart_title)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        series = QBarSeries()
        est_set = QBarSet("Estimated Hours")
        est_set.setColor("#29B2A9")
        act_set = QBarSet("Actual Hours")
        act_set.setColor("#E44164")

        categories = list(emp_data.keys())
        est_values, act_values = [], []
        for emp_name, metrics in emp_data.items():
            est_values.append(metrics["total_estimated"])
            act_values.append(metrics["total_actual"])

        est_set.append(est_values or [0])
        act_set.append(act_values or [0])
        series.append(est_set)
        series.append(act_set)
        chart.addSeries(series)

        category_axis = QBarCategoryAxis()
        category_axis.append(categories or ["No employee hours."])

        value_axis = QValueAxis()
        max_val = max(est_values + act_values) if (est_values and act_values) else 10
        value_axis.setRange(0, max(1, int(max_val * 1.1)))
        value_axis.setLabelFormat("%d")

        chart.addAxis(category_axis, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(value_axis, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(category_axis)
        series.attachAxis(value_axis)

        if clickable:
            chart_view = ClickableChartView(chart)
            chart_view.clicked.connect(lambda fuser=filter_user: self.hours_chart_modal(
                "My Workload & Hours" if fuser else "Employee Workload", 
                self._create_employee_hours_chart, 
                fuser
            ))
        else:
            chart_view = QChartView(chart)

        chart_view.setObjectName("DashboardChartView")
        chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        chart_view.setMinimumWidth(0)
        chart_view.setMinimumHeight(250)

        return chart_view


    def chart_modal(self, title, grouped_counts):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(1000, 700)

        layout = QVBoxLayout(dialog)
        layout.addWidget(self._create_status_chart(title, grouped_counts, clickable=False))

        dialog.exec()

    def hours_chart_modal(self, title, create_modal, filter_user):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(1000, 700)

        layout = QVBoxLayout(dialog)
        layout.addWidget(create_modal(filter_user=filter_user, clickable=False))

        dialog.exec()