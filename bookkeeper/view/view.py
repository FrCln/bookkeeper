"""Модуль, содержащий View часть"""
# pylint: disable=too-many-instance-attributes
# pylint: disable=c-extension-no-member
import sys
from typing import Callable

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
        self._setup_app()
        self._setup_main_window()
        self._setup_cat_window()

    def _setup_main_window(self) -> None:
        self.expense_table = ExpenseTableBox()
        self.budget_table = BudgetTableBox()
        self.expense_add = ExpenseAddBox()

        self.main_window = MainWindow(
            [self.expense_table,
             self.budget_table,
             self.expense_add]
        )

    def _setup_app(self) -> None:
        self.app = QtWidgets.QApplication(sys.argv)

    def _setup_cat_window(self) -> None:
        self.category_window = CategoryEditWindow()

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
        self.category_window.show()

    def set_categories(self, categories: list[Category]) -> None:
        """
        Загрузка данных о категориях в таблицу расходов и виджет для добавления расходов
        """
        self.expense_add.set_categories(categories)
        self.expense_table.set_categories(categories)

    def set_cat_edit_open_callback(self, callback: Callable[[], None]) -> None:
        """
        Установка обработчика событий при открытии окна редактирования категорий
        """
        self.expense_add.set_new_window_callback(callback)

    def set_cat_edit_save_callback(self, callback: Callable[[str], None]) -> None:
        """
        Установка обработчика событий при сохранении новых категорий
        """
        self.category_window.set_save_callback(callback)

    def set_cat_text(self, text: str) -> None:
        """
        Установка текста в текстовое поле категорий окна для редактирования категорий
        """
        self.category_window.set_text(text)

    def set_expenses(self, expenses: list[Expense]) -> None:
        """
        Загрузка данных о расходах в соответсвующую таблицу
        """
        self.expense_table.set_expenses(expenses)

    def set_exp_add_callback(self, exp_add_callback: Callable[[str, str], None]) -> None:
        """
        Установка обработчика событий при добавлении расхода
        """
        self.expense_add.set_exp_add_callback(exp_add_callback)

    def set_exp_table_changed_callback(
            self, callback: Callable[[int, str, str], None]
    ) -> None:
        """
        Установка обработчика событий при изменении значения ячейки таблицы расходов
        """
        self.expense_table.set_exp_table_changed_callback(callback)

    def set_budget(self, budgets: list[Budget]) -> None:
        """
        Загрузка данных о бюджете в соответствующую таблицу
        """
        self.budget_table.set_budget(budgets)

    def set_budget_table_changed_callback(
            self, callback: Callable[[str, str, str], None]
    ) -> None:
        """
        Установка обработчика событий при изменении значения ячейки таблицы бюджета
        """
        self.budget_table.set_budget_table_changed_callback(callback)
