"""
Модуль содержит класс виджета для добавления расхода
"""
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton


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
        layout.addRow("Дата:", self.date_edit)

        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Введите описание")
        layout.addRow("Description:", self.description_edit)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Еда",
                                      "Транспорт",
                                      "Развлечения",
                                      "Дом",
                                      "Другое"])
        layout.addRow("Категория:", self.category_combo)

        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("0.00")
        layout.addRow("Количество:", self.amount_edit)

        # кнопка для добавления расхода
        self.add_button = QPushButton("Добавить расход")
        self.add_button.clicked.connect(self._on_add_button_clicked)
        layout.addRow(self.add_button)

        # добавляет лейаут формы к основному лейауту
        self.setLayout(layout)

    def _on_add_button_clicked(self) -> None:
        date = self.date_edit.text()
        description = self.description_edit.text()
        category = self.category_combo.currentText()
        amount = float(self.amount_edit.text())
        self.expense_added.emit(date, description, category, amount)

        # очищает форму после добавления расхода
        self.date_edit.clear()
        self.description_edit.clear()
        self.amount_edit.clear()
        self.category_combo.setCurrentIndex(0)
