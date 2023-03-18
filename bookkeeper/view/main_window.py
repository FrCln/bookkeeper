"""Модуль, содержащий главный виджет"""
# pylint: disable=c-extension-no-member
# pylint: disable=too-few-public-methods
from typing import Any
from PySide6 import QtWidgets


class MainWindow(QtWidgets.QWidget):
    """
    Главный виджет для отображения блоков приложения
    """
    def __init__(self,
                 widgets: list[QtWidgets.QGroupBox],
                 *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Bookkeeper")
        self.resize(800, 600)

        layout = QtWidgets.QVBoxLayout()
        for i in widgets:
            layout.addWidget(i)

        self.setLayout(layout)
        self.show()
