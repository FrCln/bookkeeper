"""Модуль, содержащий виджеты для отображения инструментов для добавления расходов"""
# pylint: disable=c-extension-no-member
from typing import Any, Callable
from PySide6 import QtWidgets


class ExpenseAddLayout(QtWidgets.QGridLayout):
    """
    Расположение виджетов для добавления расходов
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.price = QtWidgets.QLineEdit()
        self.category = QtWidgets.QComboBox()

        self.add_button = QtWidgets.QPushButton("Добавить")
        self.category_edit = QtWidgets.QPushButton("Редактировать категории")
        self.category_edit.setMaximumWidth(200)

        self.addWidget(QtWidgets.QLabel("Сумма"), 0, 0)
        self.addWidget(QtWidgets.QLabel("Категория"), 1, 0)

        self.addWidget(self.price, 0, 1)
        self.addWidget(self.category, 1, 1)

        self.addWidget(self.category_edit, 1, 2)

        self.addWidget(self.add_button, 2, 0, 1, 2)

    def set_new_window_callback(self, callback: Callable[[], None]) -> None:
        """
        Устанавливает функцию для открытия окна редактирования категорий
        """
        self.category_edit.clicked.connect(callback)


class ExpenseAddBox(QtWidgets.QGroupBox):
    """
    Группа, содержащая виджеты для добавления расходов и заголовок
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setTitle("Добавление расходов")

        self.self_layout = ExpenseAddLayout()
        self.setLayout(self.self_layout)

    def set_new_window_callback(self, callback: Callable[[], None]) -> None:
        """
        Устанавливает функцию для открытия окна редактирования категорий
        """
        self.self_layout.set_new_window_callback(callback)
