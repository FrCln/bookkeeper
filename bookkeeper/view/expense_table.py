"""Модуль, содержащий виджеты для отображения таблицы с расходами"""
# pylint: disable=c-extension-no-member
from typing import Any
from PySide6 import QtWidgets


class ExpenseTableWidget(QtWidgets.QTableWidget):
    """
    Таблица расходов
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        header_labels = [
            "Сумма", "Категория", "Дата расхода", "Дата добавления", "Комментарий"
        ]
        self.setColumnCount(len(header_labels))
        self.setHorizontalHeaderLabels(header_labels)

        for i in range(len(header_labels) - 1):
            self.horizontalHeader().setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
            )

        self.horizontalHeader().setSectionResizeMode(
            len(header_labels) - 1, QtWidgets.QHeaderView.ResizeMode.Stretch
        )


class ExpenseTableBox(QtWidgets.QGroupBox):
    """
    Группа, содержащая таблицу расходов и заголовок
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setTitle("Последние расходы")

        self.table = ExpenseTableWidget()

        self.self_layout = QtWidgets.QVBoxLayout()
        self.self_layout.addWidget(self.table)
        self.setLayout(self.self_layout)
