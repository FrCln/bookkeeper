from typing import Any, List, Tuple

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
    expense_added = pyqtSignal(str, str, int)

    def __init__(self) -> None:
        super().__init__()

        # создаёт лейаут для размещения полей расходов
        layout = QFormLayout()

        # строка для ввода комментария о расходе
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Введите комментарий")
        self.description_edit.textChanged.connect(self._update_add_button_state)
        layout.addRow("Комментарий:", self.description_edit)

        self.category_combo = QComboBox()
        self.category_combo.currentIndexChanged.connect(self._update_add_button_state)
        layout.addRow("Категория:", self.category_combo)

        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("0000")
        self.amount_edit.textChanged.connect(self._update_add_button_state)
        layout.addRow("Сумма расхода:", self.amount_edit)

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
        if (self.description_edit.text() and
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
        description = self.description_edit.text()
        category = self.category_combo.currentText()
        amount_str = self.amount_edit.text()

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

        self.expense_added.emit(description, category, amount)

        # очищает форму после добавления расхода
        self.description_edit.clear()
        self.amount_edit.clear()
        self.category_combo.setCurrentIndex(0)
        self.add_button.setEnabled(False)
        return None

    def set_categories(self, categories: List[Tuple[int, str]]) -> None:
        """
        Устанавливает категории в выпадающий список
        """
        self.category_combo.clear()
        self.categories = categories
        self.category_combo.addItems([name for _, name in categories])
        self.category_combo.close
