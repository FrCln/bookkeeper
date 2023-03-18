"""Модуль, содержащий View часть"""
# pylint: disable=too-many-instance-attributes
# pylint: disable=c-extension-no-member
import sys

from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.view.budget_table import BudgetTableBox
from bookkeeper.view.category_edit import CategoryEditWindow
from bookkeeper.view.expense_add import ExpenseAddBox
from bookkeeper.view.expense_table import ExpenseTableBox
from bookkeeper.view.main_window import MainWindow


class View:
    """
    Класс, описывающий отображение (View)
    """
    def __init__(self) -> None:
        self.categories: list[Category] = []
        self.expenses: list[Expense] = []
        self.budgets: list[Budget] = []

        self._setup_app()
        self._setup_main_window()

    def _setup_main_window(self) -> None:
        self.expense_table = ExpenseTableBox()
        self.budget_table = BudgetTableBox()
        self.expense_add = ExpenseAddBox()
        self.expense_add.set_new_window_callback(self.show_category_edit_window)

        self.main_window = MainWindow(
            [self.expense_table,
             self.budget_table,
             self.expense_add]
        )

    def _setup_app(self) -> None:
        self.app = QtWidgets.QApplication(sys.argv)

    def run(self) -> None:
        """
        Запускает главное приложение
        """
        self.main_window.show()
        sys.exit(self.app.exec())

    def show_category_edit_window(self) -> None:
        """
        Открывает окно для редактирования категорий
        """
        self.category_window = CategoryEditWindow()
        self.category_window.show()


if __name__ == "__main__":
    View().run()
