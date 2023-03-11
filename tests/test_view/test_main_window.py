"""
Здесь содержатся тесты для главного окна
"""
import pytest

from PyQt6.QtWidgets import QTabWidget

from bookkeeper.view.expenses_list_widget import ExpensesListWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.add_expense_widget import AddExpenseWidget
from bookkeeper.view.category_widget import CategoryWidget


@pytest.fixture
def qtab_widget(qtbot):
    tab_widget = QTabWidget()
    expenses_list = ExpensesListWidget()
    add_expense = AddExpenseWidget()
    budget = BudgetWidget()
    category = CategoryWidget()

    tab_widget.addTab(expenses_list, "Расходы")
    tab_widget.addTab(add_expense, "Добавить расход")
    tab_widget.addTab(budget, "Бюджет")
    tab_widget.addTab(category, "Категория")

    qtbot.addWidget(tab_widget)
    return tab_widget


def test_qtab_widget(qtab_widget, qtbot):
    assert qtab_widget.count() == 4

    qtab_widget.setCurrentIndex(1)
    assert qtab_widget.currentWidget() == qtab_widget.widget(1)

    qtab_widget.setCurrentIndex(2)
    assert qtab_widget.currentWidget() == qtab_widget.widget(2)

    qtab_widget.setCurrentIndex(3)
    assert qtab_widget.currentWidget() == qtab_widget.widget(3)

    qtab_widget.setCurrentIndex(0)
    assert qtab_widget.currentWidget() == qtab_widget.widget(0)


