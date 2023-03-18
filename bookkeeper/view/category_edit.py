"""Модуль, содержащий виджеты для редактирования категорий"""
# pylint: disable=c-extension-no-member
# mypy: disable-error-code="attr-defined"
from typing import Any, Callable
from PySide6 import QtWidgets


class CategoryEditLayout(QtWidgets.QVBoxLayout):
    """
    Расположение виджетов для редактирования категорий
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.save_callback: Callable[[str], None] | None = None

        self.text_edit = QtWidgets.QTextEdit()
        self.update_button = QtWidgets.QPushButton("Сохранить")
        self.update_button.clicked.connect(self.button_callback)

        self.addWidget(self.text_edit)
        self.addWidget(self.update_button)

    def button_callback(self) -> None:
        """
        Вызов обработчика событий при нажатии на кнопку
        """
        if self.save_callback:
            self.save_callback(self.text_edit.toPlainText())

    def set_save_callback(self, callback: Callable[[str], None]) -> None:
        """
        Установка обработчика событий при нажатии на кнопку сохранения категорий
        """
        self.save_callback = callback


class CategoryEditWindow(QtWidgets.QWidget):
    """
    Окно редактирования категорий
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Редактирование категорий")

        self.self_layout = CategoryEditLayout()
        self.setLayout(self.self_layout)

    def set_text(self, text: str) -> None:
        """
        Установка текста в текстовое поле категорий
        """
        self.self_layout.text_edit.setText(text)

    def set_save_callback(self, callback: Callable[[str], None]) -> None:
        """
        Установка обработчика событий при нажатии на кнопку Сохранить
        """
        self.self_layout.set_save_callback(callback)
