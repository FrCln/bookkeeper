from datetime import datetime
from typing import List

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.view import main_window
from bookkeeper.view.expenses_list_widget import ExpensesListWidget
from bookkeeper.view.category_widget import CategoryWidget
from bookkeeper.view.add_expense_widget import AddExpenseWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.main_window import MainWindow


class Presenter:
    """
    Presenter Bookkeeper, связывает MODEL и VIEW.
    """

    def __init__(self, exp_repo: AbstractRepository[Expense],
                 cat_repo: AbstractRepository[Category]) -> None:
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo

    def show_main_window(self):
        # Create the main window
        self.main_window = MainWindow()

        # инициализирует таблицу
        self.init_table()

        # Connect the signals and slots
        self.main_window.expenses_list_widget.delete_button_clicked.connect(self.delete_expense)

        # Load the initial data into the widgets
        self.update_expenses_list()

        # Add the expenses list widget to the main window
        self.main_window.setCentralWidget(self.main_window.expenses_list_widget)

        # Show the main window
        self.main_window.show()

    def init_table(self) -> None:
        self.main_window.expenses_list_widget.init_table()

    def update_expenses_list(self) -> None:
        """
        Обновляет содержимое таблицы расходов
        на основе данных из репозитория.
        """

        objects = self.exp_repo.get_all()
        expenses = [expense for expense in objects if isinstance(expense, Expense)]
        expenses_dict = []
        # сопоставьте объекты Expense со словарём в виджете
        for expense in expenses:
            category = self.cat_repo.get(expense.category)
            expense_dict = {
                "date": datetime.strptime(expense.expense_date, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d"),
                "description": expense.comment,
                "category": str(category.name),
                "amount": str(expense.amount)
            }
            expenses_dict.append(expense_dict)
        self.main_window.expenses_list_widget.update_table(expenses_dict)

    def delete_expense(self, index: int) -> None:
        """
        Удаляет расход из базы данных и обновляет содержимое таблицы.
        """
        print(f"delete_expense called with index={index}")
        try:
            objects = self.exp_repo.get_all()
            expenses = [expense for expense in objects if isinstance(expense, Expense)]
            expense = expenses[index]
            self.exp_repo.delete(expense.pk)
            self.update_expenses_list()
        except Exception as e:
            print(f"Error deleting expense: {e}")
