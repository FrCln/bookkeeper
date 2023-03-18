from bookkeeper.view.budget_table import BudgetTableBox
from bookkeeper.view.expense_add import ExpenseAddBox
from bookkeeper.view.expense_table import ExpenseTableBox
from bookkeeper.view.main_window import MainWindow


def test_main_window(qtbot):
    expense_table = ExpenseTableBox()
    budget_table = BudgetTableBox()
    expense_add = ExpenseAddBox()

    widget = MainWindow(widgets=[
        expense_table,
        budget_table,
        expense_add
    ])
    qtbot.addWidget(widget)

    assert widget.layout().itemAt(0).widget() == expense_table
    assert widget.layout().itemAt(1).widget() == budget_table
    assert widget.layout().itemAt(2).widget() == expense_add
