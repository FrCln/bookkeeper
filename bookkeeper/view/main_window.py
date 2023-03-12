"""
MainWindow view
"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget)

from .expence_widget import ExpenceWidget
from .budget_widget import BudgetWidget
from .edit_ctg_window import EditCtgWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bookkeeper")

        layout = QtWidgets.QVBoxLayout()

        edit_field = EditCtgWindow([])
        expence = ExpenceWidget(edit_field)
        edit_field.ctg_changed.connect(expence.update_ctgs)
        budget = BudgetWidget(expence.presenter)
        expence.exp_changed.connect(budget.retrieve_exp)

        edit_layout = QtWidgets.QHBoxLayout()
        edit_layout.addWidget(budget)
        edit_layout.addWidget(edit_field)
        edit_widget = QWidget()
        edit_widget.setLayout(edit_layout)

        layout.addWidget(expence)
        layout.addWidget(edit_widget)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
