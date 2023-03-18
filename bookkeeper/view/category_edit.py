"""Модуль, содержащий виджеты для редактирования категорий"""
# pylint: disable=c-extension-no-member
from typing import Any
from PySide6 import QtWidgets


class CategoryEditLayout(QtWidgets.QVBoxLayout):
    """
    Расположение виджетов для редактирования категорий
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.text_edit = QtWidgets.QTextEdit()
        self.update_button = QtWidgets.QPushButton("Сохранить")

        self.addWidget(self.text_edit)
        self.addWidget(self.update_button)


class CategoryEditWindow(QtWidgets.QWidget):
    """
    Окно редактирования категорий
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Редактирование категорий")

        self.self_layout = CategoryEditLayout()
        self.setLayout(self.self_layout)
