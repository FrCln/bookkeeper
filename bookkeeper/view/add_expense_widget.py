"""
Модуль содержит класс виджета для добавления расхода
"""
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton


class AddExpenseWidget(QWidget):
    """
    Виджет для отображения возможности
    добавления расхода в список расходов
    """
    def __init__(self) -> None:
        super().__init__()

        # создаёт лейаут для размещения полей расходов
        layout = QFormLayout()

        # строки для  ввода информации о расходах
        date_edit = QLineEdit()
        date_edit.setPlaceholderText("YYYY-MM-DD")
        layout.addRow("Date:", date_edit)

        description_edit = QLineEdit()
        description_edit.setPlaceholderText("Enter description")
        layout.addRow("Description:", description_edit)

        category_combo = QComboBox()
        category_combo.addItems(["Food",
                                 "Transportation",
                                 "Entertainment",
                                 "Housing",
                                 "Other"])
        layout.addRow("Category:", category_combo)

        amount_edit = QLineEdit()
        amount_edit.setPlaceholderText("0.00")
        layout.addRow("Amount:", amount_edit)

        # кнопка для добавления расхода
        add_button = QPushButton("Add Expense")
        layout.addRow(add_button)

        # добавляет лейаут формы к основному лейауту
        self.setLayout(layout)
