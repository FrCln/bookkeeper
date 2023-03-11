"""
Модуль содержит класс виджета для добавления расхода
"""
from datetime import datetime
from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
)


class AddExpenseWidget(QWidget):
    """
    Виджет для отображения возможности
    добавления расхода в список расходов
    """
    expense_added = pyqtSignal(str, str, str, float)

    def __init__(self) -> None:
        super().__init__()

        # создаёт лейаут для размещения полей расходов
        layout = QFormLayout()

        # строки для ввода информации о расходах
        self.date_edit = QLineEdit()
        self.date_edit.setPlaceholderText("YYYY-MM-DD")
        self.date_edit.textChanged.connect(self._update_add_button_state)
        layout.addRow("Дата:", self.date_edit)

        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Введите описание")
        self.description_edit.textChanged.connect(self._update_add_button_state)
        layout.addRow("Description:", self.description_edit)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Еда",
                                      "Транспорт",
                                      "Развлечения",
                                      "Дом",
                                      "Другое"])
        self.category_combo.currentIndexChanged.connect(self._update_add_button_state)
        layout.addRow("Категория:", self.category_combo)

        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("0.00")
        self.amount_edit.textChanged.connect(self._update_add_button_state)
        layout.addRow("Количество:", self.amount_edit)

        # кнопка для добавления расхода
        self.add_button = QPushButton("Добавить расход")
        self.add_button.clicked.connect(self._on_add_button_clicked)
        self.add_button.setEnabled(False)
        layout.addRow(self.add_button)

        # добавляет лейаут формы к основному лейауту
        self.setLayout(layout)

    def _update_add_button_state(self) -> None:
        """
        Обновляет состояние кнопки "Добавить расходы"
        в зависимости от того, заполнены ли все обязательные поля
        """
        if (self.date_edit.text() and
                self.description_edit.text() and
                self.category_combo.currentText() and
                self.amount_edit.text()):
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def _on_add_button_clicked(self) -> Any:
        """
        Проверяет вводимые пользователем данные
        и выдаёт разные ошибки
        """
        date_str = self.date_edit.text()
        description = self.description_edit.text()
        category = self.category_combo.currentText()
        amount_str = self.amount_edit.text()

        if not self._is_valid_date(date_str):
            message_box = QMessageBox.warning(self,
                                              "Неверный формат даты",
                                              "Дата должна быть в формате YYYY-MM-DD!")
            return message_box

        try:
            amount = float(amount_str)
            if amount <= 0:
                message_box = QMessageBox.warning(self,
                                                  "Неверный формат количества",
                                                  "Количество должно быть больше нуля!")
                return message_box
        except ValueError:
            message_box = QMessageBox.warning(self,
                                              "Неверный формат количества",
                                              "Количество должно быть в формате числа!")
            return message_box

        if datetime.strptime(date_str, "%Y-%m-%d") > datetime.now():
            message_box = QMessageBox.warning(self,
                                              "Неверный формат даты",
                                              "Дата не может быть в будущем!")
            return message_box

        self.expense_added.emit(date_str, description, category, amount)

        # очищает форму после добавления расхода
        self.date_edit.clear()
        self.description_edit.clear()
        self.amount_edit.clear()
        self.category_combo.setCurrentIndex(0)
        self.add_button.setEnabled(False)
        return None

    def _is_valid_date(self, date_str: str) -> bool:
        """
        Проверяет, находится ли строка даты в формате "YYYY-MM-DD".
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
