"""
Модуль содержит класс виджета расходов
для отображения информации о расходах таблицей.
"""
from typing import cast

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
            {"date": "2023-03-01", "description": "Продукты",
                "category": "Еда", "amount": "3000.00"},
            {"date": "2023-03-02", "description": "Питса",
                "category": "Еда", "amount": "700.00"},
            {"date": "2023-03-03", "description": "Билеты на Чебурашку",
                "category": "Развлечения", "amount": "300.00"}
        ]

        self.table = QTableWidget()
        self.init_table()
        self.update_table()

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

        day_button.clicked.connect(self.filter_day)
        week_button.clicked.connect(self.filter_week)
        month_button.clicked.connect(self.filter_month)

    def init_table(self) -> None:
        """
        инициализирует таблицу, на которой будут
        отображаться данные о расходах.
        """
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Дата", "Название", "Категория", "Количество", ""])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

        self.table.setRowCount(len(self.expenses))
        for row, expense in enumerate(self.expenses):
            date_item = QTableWidgetItem(expense["date"])
            description_item = QTableWidgetItem(expense["description"])
            category_item = QTableWidgetItem(expense["category"])
            amount_item = QTableWidgetItem(expense["amount"])
            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(self.delete_row)
            self.table.setItem(row, 0, date_item)
            self.table.setItem(row, 1, description_item)
            self.table.setItem(row, 2, category_item)
            self.table.setItem(row, 3, amount_item)
            self.table.setCellWidget(row, 4, delete_button)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

    def update_table(self) -> None:
        """
        Обновляет содержимое таблицы
        с учетом изменений в списке расходов.
        """
        self.table.setRowCount(len(self.expenses))
        for row, expense in enumerate(self.expenses):
            date_item = self.table.item(row, 0)
            description_item = self.table.item(row, 1)
            category_item = self.table.item(row, 2)
            amount_item = self.table.item(row, 3)
            delete_button = self.table.cellWidget(row, 4)
            if not all((date_item,
                        description_item,
                        category_item,
                        amount_item,
                        delete_button)):
                date_item = QTableWidgetItem(expense["date"])

                description_item = QTableWidgetItem(expense["description"])

                category_item = QTableWidgetItem(expense["category"])

                amount_item = QTableWidgetItem(expense["amount"])

                delete_button = QPushButton("Удалить")
                delete_button.clicked.connect(self.delete_row)

                self.table.setItem(row, 0, date_item)
                self.table.setItem(row, 1, description_item)
                self.table.setItem(row, 2, category_item)
                self.table.setItem(row, 3, amount_item)
                self.table.setCellWidget(row, 4, delete_button)
                self.table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

    def filter_day(self) -> None:
        """
        заглушка
        """
        pass

    def filter_week(self) -> None:
        """
        заглушка
        """
        pass

    def filter_month(self) -> None:
        """
        заглушка
        """
        pass

    def delete_row(self) -> None:
        """
        Удаляет строку с выбранным расходом из списка расходов
        и обновляет содержимое таблицы.
        """
        delete_button: QPushButton = cast(QPushButton, self.sender())
        index: int = self.table.indexAt(delete_button.pos()).row()
        if index >= 0:
            self.expenses.pop(index)
            self.update_table()
