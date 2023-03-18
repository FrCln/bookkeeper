"""Модуль, содержащий виджеты для отображения инструментов для добавления расходов"""
# pylint: disable=c-extension-no-member
# mypy: disable-error-code="attr-defined"
from typing import Any, Callable
from PySide6 import QtWidgets
from bookkeeper.models.category import Category


class ExpenseAddLayout(QtWidgets.QGridLayout):
    """
    Расположение виджетов для добавления расходов
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.add_button_callback: Callable[[str, str], None] | None = None

        self.price = QtWidgets.QLineEdit()
        self.category = QtWidgets.QComboBox()

        self.add_button = QtWidgets.QPushButton("Добавить")
        self.add_button.clicked.connect(self.button_callback)

        self.category_edit = QtWidgets.QPushButton("Редактировать категории")
        self.category_edit.setMaximumWidth(200)

        self.addWidget(QtWidgets.QLabel("Сумма"), 0, 0)
        self.addWidget(QtWidgets.QLabel("Категория"), 1, 0)

        self.addWidget(self.price, 0, 1)
        self.addWidget(self.category, 1, 1)

        self.addWidget(self.category_edit, 1, 2)

        self.addWidget(self.add_button, 2, 0, 1, 2)

    def button_callback(self) -> None:
        """
        Вызов обработчика событий при нажатии на кнопку
        """
        if self.add_button_callback:
            value1 = self.price.text()
            value2 = self.category.currentText()
            self.add_button_callback(value1, value2)

    def set_exp_add_callback(self, exp_add_callback: Callable[[str, str], None]) -> None:
        """
        Установка обработчика событий при нажатии на кнопку добавления расхода
        """
        self.add_button_callback = exp_add_callback


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
        self.self_layout.category_edit.clicked.connect(callback)

    def set_categories(self, categories: list[Category]) -> None:
        """
        Загрузка данных о категориях в виджет выбора категорий
        """
        self.self_layout.category.clear()
        self.self_layout.category.addItems([cat.name for cat in categories])

    def set_exp_add_callback(self, exp_add_callback: Callable[[str, str], None]) -> None:
        """
        Установка обработчика событий при нажатии на кнопку добавления расхода
        """
        self.self_layout.set_exp_add_callback(exp_add_callback)
