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
        tab_widget = QTabWidget()

        # виджет бюджета
        self.budget_widget = BudgetWidget()
        tab_widget.addTab(self.budget_widget, "Бюджет")

        # виджет категорий
        self.category_widget = CategoryWidget()
        tab_widget.addTab(self.category_widget, "Категории")

        # виджет расходов
        self.expenses_list_widget = ExpensesListWidget()
        tab_widget.addTab(self.expenses_list_widget, "Список расходов")

        # виджет добавления расхода
        self.add_expense_widget = AddExpenseWidget()
        tab_widget.addTab(self.add_expense_widget, "Добавить расход")

        # виджет вкладок в качестве центрального виджета главного окна
        self.setCentralWidget(tab_widget)
        self.presenter = None

    # заглушка


def set_presenter(self, presenter):
    self.presenter = presenter
