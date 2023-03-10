"""
Модуль содержит класс бюджетного виджета для отображения информации о бюджете.
"""
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QDoubleSpinBox,
    QGroupBox,
    QHBoxLayout,
    QRadioButton,
    QPushButton,
)


class BudgetWidget(QWidget):
    """
    Виджет для отображения бюджетной информации
    за разные периоды (день, неделю и месяц)
    """
    def __init__(self) -> None:
        super().__init__()

        # создаёт поле для хранения настроек бюджета
        group_box = QGroupBox("Budget")
        group_layout = QVBoxLayout()

        # для отображения текущего бюджета
        budget_label = QLabel("Current Budget: \u20bd0.00")  # символ российского рубля! Z
        group_layout.addWidget(budget_label)

        # переключатели для выбора периода времени для бюджета
        day_button = QRadioButton("Day")
        week_button = QRadioButton("Week")
        month_button = QRadioButton("Month")
        day_button.setChecked(True)  # день стоит по дефолту

        time_period_layout = QHBoxLayout()
        time_period_layout.addWidget(day_button)
        time_period_layout.addWidget(week_button)
        time_period_layout.addWidget(month_button)

        group_layout.addLayout(time_period_layout)

        # создаёте QDoubleSpinBox для установки бюджета
        self.budget_spinbox = QDoubleSpinBox()
        self.budget_spinbox.setPrefix("\u20bd")
        self.budget_spinbox.setDecimals(2)
        self.budget_spinbox.setMinimum(0.0)
        self.budget_spinbox.setMaximum(10000.0)
        self.budget_spinbox.setValue(0.0)

        group_layout.addWidget(self.budget_spinbox)

        # кнопка для подтверждения изменений
        apply_button = QPushButton("Apply")

        group_layout.addWidget(apply_button)

        group_box.setLayout(group_layout)

        layout = QVBoxLayout()
        layout.addWidget(group_box)
        self.setLayout(layout)
