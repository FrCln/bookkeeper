"""Модуль, содержащий виджеты для отображения таблицы с расходами"""
# pylint: disable=c-extension-no-member
# mypy: disable-error-code="attr-defined"
from typing import Any, Callable
from PySide6 import QtWidgets
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.utils import date_converter


class ExpenseTableWidget(QtWidgets.QTableWidget):
    """
    Таблица расходов
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.cell_changed_callback: Callable[[int, str, str], None] | None = None

        self.col_to_attr = {
            0: "amount",
            1: "category",
            2: "expense_date",
            3: "added_date",
            4: "comment"
        }

        header_labels = [
            "Сумма", "Категория", "Дата расхода", "Дата добавления", "Комментарий"
        ]

        self.setColumnCount(len(header_labels))
        self.setHorizontalHeaderLabels(header_labels)

        for i in range(len(header_labels) - 1):
            self.horizontalHeader().setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
            )

        self.horizontalHeader().setSectionResizeMode(
            len(header_labels) - 1, QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        self.cellChanged.connect(self.cell_changed)

    def cell_changed(self, row: int, column: int) -> None:
        """
        Вызов обработчика событий при изменении значения ячейки
        """
        if self.cell_changed_callback:
            self.cell_changed_callback(
                row+1,
                self.col_to_attr[column],
                self.item(row, column).text()
            )

    def set_cell_changed_callback(
            self, callback: Callable[[int, str, str], None]
    ) -> None:
        """
        Установка обработчика событий при изменении значения ячейки
        """
        self.cell_changed_callback = callback


class ExpenseTableBox(QtWidgets.QGroupBox):
    """
    Группа, содержащая таблицу расходов и заголовок
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setTitle("Последние расходы")

        self.table = ExpenseTableWidget()
        self.cat_dict: dict[int, str] = {}

        self.self_layout = QtWidgets.QVBoxLayout()
        self.self_layout.addWidget(self.table)
        self.setLayout(self.self_layout)

    def set_expenses(self, expenses: list[Expense]) -> None:
        """
        Загрузка данных о расходах в таблицу
        """
        self.table.clearContents()
        self.table.setRowCount(len(expenses))

        item = QtWidgets.QTableWidgetItem

        for exp in expenses:
            pk = exp.pk - 1
            self.table.setItem(pk, 0, item(str(exp.amount)))
            if self.cat_dict:
                self.table.setItem(pk, 1, item(self.cat_dict[exp.category]))
            else:
                self.table.setItem(pk, 1, item(str(exp.category)))
            self.table.setItem(pk, 2, item(date_converter(exp.expense_date)))
            self.table.setItem(pk, 3, item(date_converter(exp.added_date)))
            self.table.setItem(pk, 4, item(exp.comment))

    def set_categories(self, categories: list[Category]) -> None:
        """
        Загрузка данных о категориях
        """
        self.cat_dict = {cat.pk: cat.name for cat in categories}

    def set_exp_table_changed_callback(
            self, callback: Callable[[int, str, str], None]
    ) -> None:
        """
        Установка обработчика событий при изменении значения ячейки
        """
        self.table.set_cell_changed_callback(callback)
