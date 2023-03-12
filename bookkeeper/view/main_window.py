"""
MainWindow view
"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget)

from bookkeeper.view.expense_widget import ExpenseWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.edit_ctg_window import EditCtgWindow


class MainWindow(QtWidgets.QMainWindow):
    """Represents Main Window.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bookkeeper")

        layout = QtWidgets.QVBoxLayout()

        edit_field = EditCtgWindow()
        expense = ExpenseWidget(edit_field)
        edit_field.ctg_changed.connect(expense.update_ctgs)
        budget = BudgetWidget(expense.presenter)
        expense.exp_changed.connect(budget.retrieve_exp)

        edit_layout = QtWidgets.QHBoxLayout()
        edit_layout.addWidget(budget)
        edit_layout.addWidget(edit_field)
        edit_widget = QWidget()
        edit_widget.setLayout(edit_layout)

        layout.addWidget(expense)
        layout.addWidget(edit_widget)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
