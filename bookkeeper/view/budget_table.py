"""Модуль, содержащий виджеты для отображения бюджета"""
# pylint: disable=c-extension-no-member
# mypy: disable-error-code="attr-defined"
from typing import Any, Callable
from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget


class BudgetTableWidget(QtWidgets.QTableWidget):
    """
    Таблица бюджета
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.cell_changed_callback: Callable[[str, str, str], None] | None = None

        self.row_to_period = {
            0: "day",
            1: "week",
            2: "month"
        }

        self.col_to_attr = {
            0: "spent",
            1: "total"
        }

        header_labels = ["Сумма", "Бюджет"]
        first_col_labels = ["День", "Неделя", "Месяц"]

        self.setColumnCount(len(header_labels))
        self.setRowCount(len(first_col_labels))

        self.setHorizontalHeaderLabels(header_labels)
        for i in range(len(header_labels)):
            self.horizontalHeader().setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeMode.Stretch
            )

        self.setVerticalHeaderLabels(first_col_labels)
        for i in range(len(first_col_labels)):
            self.verticalHeader().setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeMode.Stretch
            )

        self.cellChanged.connect(self.cell_changed)

    def cell_changed(self, row: int, column: int) -> None:
        """
        Вызов обработчика событий при изменении значения ячейки
        """
        if self.cell_changed_callback:
            self.cell_changed_callback(
                self.row_to_period[row],
                self.col_to_attr[column],
                self.item(row, column).text()
            )

    def set_cell_changed_callback(
            self, callback: Callable[[str, str, str], None]
    ) -> None:
        """
        Установка обработчика событий при изменении значения ячейки
        """
        self.cell_changed_callback = callback


class BudgetTableBox(QtWidgets.QGroupBox):
    """
    Группа, содержащая таблицу бюджета и заголовок
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setTitle("Бюджет")

        self.table = BudgetTableWidget()

        self.self_layout = QtWidgets.QVBoxLayout()
        self.self_layout.addWidget(self.table)
        self.setLayout(self.self_layout)

        self.setMaximumHeight(self.table.height())

    def set_budget(self, budgets: list[Budget]) -> None:
        """
        Загрузка данных о бюджете в таблицу
        """
        self.table.clearContents()
        self.table.setRowCount(len(budgets))

        item = QtWidgets.QTableWidgetItem

        for row, budget in enumerate(budgets):

            self.table.setItem(row, 0, item(str(budget.spent)))
            self.table.setItem(row, 1, item(str(budget.total)))

    def set_budget_table_changed_callback(
            self, callback: Callable[[str, str, str], None]
    ) -> None:
        """
        Установка обработчика событий при изменении значения ячейки
        """
        self.table.set_cell_changed_callback(callback)
