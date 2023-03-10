"""
Модуль содержит класс виджета расходов для отображения информации о расходах таблицей.
"""
from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QWidget,
    QVBoxLayout,
    QAbstractItemView,
    QHBoxLayout,
    QPushButton,
)


class ExpensesListWidget(QWidget):
    """
    Виджет для отображения таблицы расходов.
    """
    def __init__(self) -> None:
        super().__init__()

        # просто для примера
        self.expenses = [
            {"date": "2023-03-01", "description": "Продукты", "category": "Еда", "amount": "3000.00"},
            {"date": "2023-03-02", "description": "Питса", "category": "Еда", "amount": "700.00"},
            {"date": "2023-03-03", "description": "Билеты на Чебурашку", "category": "Развлечения", "amount": "300.00"}
        ]

        # создаёт таблицу для отображения данных о расходах
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Дата", "Название", "Категория", "Количество", ""])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

        # заполняет таблицу данными о расходах
        self.table.setRowCount(len(self.expenses))
        for row, expense in enumerate(self.expenses):
            date_item = QTableWidgetItem(expense["date"])
            description_item = QTableWidgetItem(expense["description"])
            category_item = QTableWidgetItem(expense["category"])
            amount_item = QTableWidgetItem(expense["amount"])
            # добавляет кнопку «Удалить» для каждой строки
            delete_item = QPushButton("Удалить")
            self.table.setItem(row, 0, date_item)
            self.table.setItem(row, 1, description_item)
            self.table.setItem(row, 2, category_item)
            self.table.setItem(row, 3, amount_item)
            # добавляет кнопку «Удалить» для каждой строки
            self.table.setCellWidget(row, 4, delete_item)

        # позволяет пользователям редактировать каждую ячейку
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

        # добавляет кнопки фильтра
        day_button = QPushButton("День")
        week_button = QPushButton("Неделя")
        month_button = QPushButton("Месяц")

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(day_button)
        filter_layout.addWidget(week_button)
        filter_layout.addWidget(month_button)

        layout = QVBoxLayout()
        layout.addLayout(filter_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
