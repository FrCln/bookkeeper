import sys

from PyQt6.QtWidgets import QApplication

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository

from bookkeeper.bookkeeper_presenter import Presenter


def main():
    # указываем репозиторий
    exp_repo = SQLiteRepository('budget.db', Expense)
    cat_repo = SQLiteRepository('budget.db', Category)
    bud_repo = SQLiteRepository('budget.db', Budget)

    presenter = Presenter(exp_repo, cat_repo, bud_repo)

    app = QApplication(sys.argv)
    presenter.show_main_window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
