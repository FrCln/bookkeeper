import sys

from PyQt6.QtWidgets import QApplication

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository

from bookkeeper.view.expenses_list_widget import ExpensesListWidget
from bookkeeper.view.category_widget import CategoryWidget
from bookkeeper.view.add_expense_widget import AddExpenseWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.bookkeeper_presenter import Presenter
from bookkeeper.view.main_window import MainWindow


def main():
    # указываем репозиторий
    exp_repo = SQLiteRepository('budget.db', Expense)
    cat_repo = SQLiteRepository('budget.db', Category)

    presenter = Presenter(exp_repo, cat_repo)

    app = QApplication(sys.argv)
    presenter.show_main_window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
