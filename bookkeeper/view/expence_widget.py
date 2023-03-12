"""
Widget of expence table
"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QTableWidget)


def set_data(table: QTableWidget, data: list[list[str]]) -> None:
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            table.setItem(i, j, QtWidgets.QTableWidgetItem(x.capitalize()))


class ExpenceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Последние расходы")
        layout.addWidget(message)

        expenses_table = QtWidgets.QTableWidget(4, 20)
        expenses_table.setColumnCount(4)
        expenses_table.setRowCount(20)
        expenses_table.setHorizontalHeaderLabels("Дата "
                                                 "Сумма "
                                                 "Категория "
                                                 "Комментарий".split())

        header = expenses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        expenses_table.verticalHeader().hide()
        set_data(expenses_table, [])

        layout.addWidget(expenses_table)
        self.setLayout(layout)
