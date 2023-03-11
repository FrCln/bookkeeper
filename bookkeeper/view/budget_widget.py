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
        group_box = QGroupBox("Бюджет")
        group_layout = QVBoxLayout()

        # для отображения текущего бюджета
        self.budget_label = QLabel("Текущий бюджет: "
                                   "\u20bd0.00")  # символ российского рубля! Z
        group_layout.addWidget(self.budget_label)

        # переключатели для выбора периода времени для бюджета
        self.day_button = QRadioButton("День")
        self.week_button = QRadioButton("Неделя")
        self.month_button = QRadioButton("Месяц")
        self.day_button.setChecked(True)  # день стоит по дефолту

        time_period_layout = QHBoxLayout()
        time_period_layout.addWidget(self.day_button)
        time_period_layout.addWidget(self.week_button)
        time_period_layout.addWidget(self.month_button)

        group_layout.addLayout(time_period_layout)

        # создаёте QDoubleSpinBox для установки бюджета
        self.budget_spinbox = QDoubleSpinBox()
        self.budget_spinbox.setPrefix("\u20bd")
        self.budget_spinbox.setDecimals(2)
        self.budget_spinbox.setMinimum(0.0)
        self.budget_spinbox.setMaximum(100000000000000000000.0)
        self.budget_spinbox.setValue(0.0)

        group_layout.addWidget(self.budget_spinbox)

        # кнопка для подтверждения изменений
        apply_button = QPushButton("Применить")
        apply_button.clicked.connect(self.apply_budget)

        group_layout.addWidget(apply_button)

        group_box.setLayout(group_layout)

        layout = QVBoxLayout()
        layout.addWidget(group_box)
        self.setLayout(layout)

        # соединяем сигналы с методами обновления
        self.day_button.toggled.connect(self.update_budget_label)
        self.week_button.toggled.connect(self.update_budget_label)
        self.month_button.toggled.connect(self.update_budget_label)
        self.budget_spinbox.valueChanged.connect(self.update_budget_label)

    def apply_budget(self) -> None:
        """
        Метод для обработки нажатия кнопки "Применить"
        """
        # здесь добавлю логику для сохранения настроек бюджета
        pass

    def update_budget_label(self) -> None:
        """
        Метод для обновления текста метки текущего бюджета
        """
        budget = self.budget_spinbox.value()

        if self.day_button.isChecked():
            period = "День"
            budget_per_period = budget / 30
        elif self.week_button.isChecked():
            period = "Неделя"
            budget_per_period = budget / 7
        else:
            period = "Месяц"
            budget_per_period = budget

        self.budget_label.setText(
            f"Текущий бюджет ({period}): \u20bd{budget_per_period:.2f}")
