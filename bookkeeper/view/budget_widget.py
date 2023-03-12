"""
Widget of budget table
"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QTableWidget)


def set_data(table: QTableWidget, spent: list[float], day_budget: float) -> None:
    budget = [day_budget, day_budget * 7, day_budget * 30]
    for i, [lost, limit] in enumerate(zip(spent, budget)):
        table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(lost)))
        table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(limit)))


class BudgetWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Бюджет")
        layout.addWidget(message)

        expenses_table = QtWidgets.QTableWidget(2, 3)
        expenses_table.setColumnCount(2)
        expenses_table.setRowCount(3)
        expenses_table.setHorizontalHeaderLabels("Сумма "
                                                 "Бюджет ".split())
        expenses_table.setVerticalHeaderLabels("День "
                                               "Неделя "
                                               "Месяц ".split())

        header = expenses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        set_data(expenses_table, [0, 0, 0], 1)

        layout.addWidget(expenses_table)
        self.setLayout(layout)
