import sys
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from bookkeeper.view.expenses_list_widget import ExpensesListWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.add_expense_widget import AddExpenseWidget
from bookkeeper.view.category_widget import CategoryWidget


class MainWindow(QMainWindow):
    """
    Виджет для отображения главного окна.
    """

    def __init__(self):
        super().__init__()

        # создаёт QTabWidget для хранения различных виджетов
        self.expenses_list_widget = ExpensesListWidget()
        tab_widget = QTabWidget()

        # виджет расходов
        expenses_list = ExpensesListWidget()
        tab_widget.addTab(expenses_list, "Список расходов")

        # виджет добавления расхода
        add_expense = AddExpenseWidget()
        tab_widget.addTab(add_expense, "Добавить расход")

        # виджет бюджета
        budget = BudgetWidget()
        tab_widget.addTab(budget, "Бюджет")

        # виджет категорий
        category = CategoryWidget()
        tab_widget.addTab(category, "Категории")

        # виджет вкладок в качестве центрального виджета главного окна
        self.setCentralWidget(tab_widget)
        self.presenter = None



    # заглушка
def set_presenter(self, presenter):
    self.presenter = presenter
