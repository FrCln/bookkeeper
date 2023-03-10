"""
Этот код определяет класс MainWindow,
который служит главным окном для виджетов
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from bookkeeper.view.expenses_list_widget import ExpensesListWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.add_expense_widget import AddExpenseWidget
from bookkeeper.view.category_widget import CategoryWidget


class MainWindow(QMainWindow):
    """
    Виджет для отображения главного окна.
    """
    def __init__(self) -> None:
        super().__init__()

        # создаёт QTabWidget для хранения различных виджетов
        tab_widget = QTabWidget()

        # виджет расходов
        expenses_list = ExpensesListWidget()
        tab_widget.addTab(expenses_list, "Expenses")

        # виджет добавления расхода
        add_expense = AddExpenseWidget()
        tab_widget.addTab(add_expense, "Add Expense")

        # виджет бюджета
        budget = BudgetWidget()
        tab_widget.addTab(budget, "Budget")

        # виджет категорий
        category = CategoryWidget()
        tab_widget.addTab(category, "Categories")

        # виджет вкладок в качестве центрального виджета главного окна
        self.setCentralWidget(tab_widget)


# создаёт приложение и показывает главное окно
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
