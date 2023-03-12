"""
Widget of editing categories
"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QListWidget)


def set_data(table: QListWidget, data: list[str]) -> None:
    for ctg in data:
        table.addItem(ctg)


class EditCtgWindow(QWidget):
    def __init__(self, ctgs: list[str]) -> None:
        super().__init__()
        
        self.setWindowTitle("Изменение категорий")

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Категории")
        layout.addWidget(message)

        ctgs_widget = QtWidgets.QListWidget()
        set_data(ctgs_widget, ctgs)

        layout.addWidget(ctgs_widget)
        self.setLayout(layout)
