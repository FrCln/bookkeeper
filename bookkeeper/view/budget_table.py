"""Модуль, содержащий виджеты для отображения бюджета"""
# pylint: disable=c-extension-no-member
from typing import Any
from PySide6 import QtWidgets


class BudgetTableWidget(QtWidgets.QTableWidget):
    """
    Таблица бюджета
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        header_labels = ["Сумма", "Бюджет"]
        first_col_labels = ["День", "Неделя", "Месяц"]

        self.setColumnCount(len(header_labels))
        self.setRowCount(len(first_col_labels))

        self.setHorizontalHeaderLabels(header_labels)
        for i in range(len(header_labels)):
            self.horizontalHeader().setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeMode.Stretch
            )

        self.setVerticalHeaderLabels(first_col_labels)
        for i in range(len(first_col_labels)):
            self.verticalHeader().setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeMode.Stretch
            )


class BudgetTableBox(QtWidgets.QGroupBox):
    """
    Группа, содержащая таблицу бюджета и заголовок
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setTitle("Бюджет")

        self.table = BudgetTableWidget()

        self.self_layout = QtWidgets.QVBoxLayout()
        self.self_layout.addWidget(self.table)
        self.setLayout(self.self_layout)

        self.setMaximumHeight(self.table.height())
