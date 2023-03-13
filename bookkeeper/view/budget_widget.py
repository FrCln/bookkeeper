"""
Модуль содержит класс бюджетного виджета для отображения информации о бюджете.
"""
from PyQt6.QtCore import QDate, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QGroupBox,
    QGridLayout,
)


class BudgetWidget(QWidget):
    """
    Виджет для отображения информации о бюджете
    за разные периоды (день, неделю и месяц).
    """
    day_budget_edited = pyqtSignal(float)
    week_budget_edited = pyqtSignal(float)
    month_budget_edited = pyqtSignal(float)

    expenses_updated = pyqtSignal(float, float, float)

    def __init__(self) -> None:
        super().__init__()

        current_month = QDate.currentDate().toString("MMMM yyyy")
        self.month_label = QLabel(f"Бюджет за {current_month}")
        self.month_label.setStyleSheet("font-size: 36px; font-weight: bold;")

        self.month_budget_label = QLabel("\u20bd0.00")
        self.month_budget_label.setStyleSheet("font-size: 24px;")

        self.week_label = QLabel("Бюджет на неделю:")
        self.week_label.setStyleSheet("font-size: 16px;")

        self.week_budget_label = QLabel("\u20bd0.00")
        self.week_budget_label.setStyleSheet("font-size: 14px;")

        self.day_label = QLabel("Бюджет за день:")
        self.day_label.setStyleSheet("font-size: 16px;")

        self.day_budget_label = QLabel("\u20bd0.00")
        self.day_budget_label.setStyleSheet("font-size: 14px;")

        group_box = QGroupBox("ЗАДАТЬ НОВЫЙ БЮДЖЕТ:")
        group_layout = QGridLayout()

        day_budget_label = QLabel("Задать бюджет на день:")
        day_budget_label.setStyleSheet("font-size: 12px;")
        self.day_budget_edit = QLineEdit()
        self.day_budget_edit.setPlaceholderText("\u20bd0.00")

        week_budget_label = QLabel("Задать бюджет на неделю:")
        week_budget_label.setStyleSheet("font-size: 12px;")
        self.week_budget_edit = QLineEdit()
        self.week_budget_edit.setPlaceholderText("\u20bd0.00")

        month_budget_label = QLabel("Задать бюджет на месяц:")
        month_budget_label.setStyleSheet("font-size: 12px;")
        self.month_budget_edit = QLineEdit()
        self.month_budget_edit.setPlaceholderText("\u20bd0.00")

        group_layout.addWidget(day_budget_label, 0, 0)
        group_layout.addWidget(self.day_budget_edit, 0, 1)
        group_layout.addWidget(week_budget_label, 1, 0)
        group_layout.addWidget(self.week_budget_edit, 1, 1)
        group_layout.addWidget(month_budget_label, 2, 0)
        group_layout.addWidget(self.month_budget_edit, 2, 1)
        group_box.setLayout(group_layout)

        expenses_group_box = QGroupBox("РАСХОДЫ:")
        expenses_layout = QVBoxLayout()
        expenses_group_box.setLayout(expenses_layout)

        self.day_expenses_label = QLabel("Расходы за день: \u20bd0.00")
        self.week_expenses_label = QLabel("Расходы за неделю: \u20bd0.00")
        self.month_expenses_label = QLabel("Расходы за месяц: \u20bd0.00")
        expenses_layout.addWidget(self.day_expenses_label)
        expenses_layout.addWidget(self.week_expenses_label)
        expenses_layout.addWidget(self.month_expenses_label)

        layout = QVBoxLayout()
        layout.addWidget(self.month_label)
        layout.addWidget(self.month_budget_label)
        layout.addWidget(self.week_label)
        layout.addWidget(self.week_budget_label)
        layout.addWidget(self.day_label)
        layout.addWidget(self.day_budget_label)
        layout.addWidget(group_box)
        layout.addWidget(expenses_group_box)
        self.setLayout(layout)

        self.day_budget_edit.editingFinished.connect(lambda: self.update_day_budget(float(self.day_budget_edit.text())))
        self.week_budget_edit.editingFinished.connect(
            lambda: self.update_week_budget(float(self.week_budget_edit.text())))
        self.month_budget_edit.editingFinished.connect(
            lambda: self.update_month_budget(float(self.month_budget_edit.text())))

        self.expenses_updated.connect(self.update_expenses_labels)

    def set_month_budget(self, value: float) -> None:
        """
        Устанавливает бюджет на месяц заголовком
        """
        self.month_budget_label.setText(f"\u20bd{value:.2f}")

    def set_month(self, year: int, month: int) -> None:
        """
        Устанавливает какой месяц и день отображать
        """
        month_name = QDate(year, month, 1).toString("MMMM yyyy")
        self.month_label.setText(f"Бюджет за {month_name}")

    def update_day_budget(self, value: str) -> None:
        """
        Метод для обновления бюджета за день
        """
        try:
            day_budget = float(value)
            self.day_budget_edited.emit(day_budget)
        except ValueError as e:
            print(e)

    def update_week_budget(self, value: str) -> None:
        """
        Метод для обновления недельного бюджета
        """
        try:
            week_budget = float(value)
            self.week_budget_edited.emit(week_budget)
        except ValueError as e:
            print(e)

    def update_month_budget(self, value: str) -> None:
        """
        Метод для обновления месячного бюджета
        """
        try:
            month_budget = float(value)
            self.month_budget_edited.emit(month_budget)
        except ValueError as e:
            print(e)

    def update_expenses_labels(self, day_expenses: float,
                               week_expenses: float,
                               month_expenses: float) -> None:
        """
        Метод для обновления месячных расходов
        """

        self.day_expenses_label.setText(f"Расходы за день: \u20bd{day_expenses:.2f}")
        self.week_expenses_label.setText(f"Расходы за неделю: \u20bd{week_expenses:.2f}")
        self.month_expenses_label.setText(f"Расходы за месяц: \u20bd{month_expenses:.2f}")

