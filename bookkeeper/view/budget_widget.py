"""
Widget of budget table
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QMessageBox)
from .presenters import BudgetPresenter
from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.budget import Budget


class LimitDayItem(QTableWidgetItem):
    def __init__(self, bgt: Budget):
        super().__init__()
        self.update(bgt)

    def get_value(self):
        try:
            return float(self.text())
        except ValueError:
            return None

    def update(self, bgt: Budget):
        self.bgt = bgt
        self.setText(str(self.bgt.amount))
        pass


class LimitWeekItem(QTableWidgetItem):
    def __init__(self, bgt: Budget):
        super().__init__()
        self.update(bgt)

    def get_value(self):
        try:
            return float(self.text()) / 7
        except ValueError:
            return None

    def update(self, bgt: Budget):
        self.bgt = bgt
        self.setText(str(self.bgt.amount * 7))
        pass


class LimitMonthItem(QTableWidgetItem):
    def __init__(self, bgt: Budget):
        super().__init__()
        self.update(bgt)

    def get_value(self):
        try:
            return float(self.text()) / 30
        except ValueError:
            return None

    def update(self, bgt: Budget):
        self.bgt = bgt
        self.setText(str(self.bgt.amount * 30))
        pass


class BudgetWidget(QWidget):
    def __init__(self, exp_presenter) -> None:
        super().__init__()
        self.exp_presenter = exp_presenter

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Бюджет")
        layout.addWidget(message)

        self.expenses_table = QtWidgets.QTableWidget(2, 3)
        self.expenses_table.setColumnCount(2)
        self.expenses_table.setRowCount(3)
        self.expenses_table.setHorizontalHeaderLabels("Сумма "
                                                      "Бюджет ".split())
        self.expenses_table.setVerticalHeaderLabels("День "
                                                    "Неделя "
                                                    "Месяц ".split())

        header = self.expenses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        for i in range(3):
            lost_item = QtWidgets.QTableWidgetItem()
            lost_item.setFlags(lost_item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.expenses_table.setItem(i, 0, lost_item)
        
        bgt: Budget = Budget(1)
        self.expenses_table.setItem(0, 1, LimitDayItem(bgt))
        self.expenses_table.setItem(1, 1, LimitWeekItem(bgt))
        self.expenses_table.setItem(2, 1, LimitMonthItem(bgt))
        self.expenses_table.itemChanged.connect(self.edit_bgt_event)

        layout.addWidget(self.expenses_table)
        self.setLayout(layout)

        self.presenter = BudgetPresenter(self, RepositoryFactory())

        expenses = self.exp_getter()
        bgt = self.bgt_getter()

        self.update_expenses(expenses)
        self.update_budget(bgt)
    
    def register_bgt_getter(self, handler):
        self.bgt_getter = handler
    
    def register_bgt_modifier(self, handler):
        self.bgt_modifier = handler

    def register_exp_getter(self, handler):
        self.exp_getter = handler

    def edit_bgt_event(self, bgt_item: QTableWidgetItem):
        value = bgt_item.get_value()
        if value is None:
            QMessageBox.critical(self, 'Ошибка', 'Используйте только числа.')
        else:
            bgt_item.bgt.amount = value
            self.bgt_modifier(bgt_item.bgt)

        self.update_budget(bgt_item.bgt)

    def update_expenses(self, exps: list[float]) -> None:
        self.expenses_table.itemChanged.disconnect()
        assert len(exps) == 3
        for i, exp in enumerate(exps):
            self.expenses_table.item(i, 0).setText(str(exp))
        self.expenses_table.itemChanged.connect(self.edit_bgt_event)

    def update_budget(self, bgt: Budget) -> None:
        self.expenses_table.itemChanged.disconnect()
        for i in range(3):
            self.expenses_table.item(i, 1).update(bgt)
        self.expenses_table.itemChanged.connect(self.edit_bgt_event)

    def retrieve_exp(self):
        self.update_expenses(self.exp_getter())
