import pytest
from datetime import datetime, timedelta

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.expense_table import ExpenseTableBox, ExpenseTableWidget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category


@pytest.fixture
def get_callback():
    def callback(val1: int, val2: str, val3: str) -> None:
        callback.val1 = val1
        callback.val2 = val2
        callback.val3 = val3

    return callback


@pytest.fixture
def exp_repo():
    repo = MemoryRepository()
    [repo.add(Expense(category=i+1, amount=i)) for i in range(5)]
    return repo


@pytest.fixture
def cat_repo():
    repo = MemoryRepository()
    [repo.add(Category(name=f"cat{i}")) for i in range(5)]
    return repo


def test_set_expenses(qtbot, exp_repo):
    widget = ExpenseTableBox()
    qtbot.addWidget(widget)

    widget.set_expenses(exp_repo.get_all())

    data = exp_repo.get_all()

    for i in range(widget.table.rowCount()):
        exp: Expense = data[i]

        assert exp.amount == int(widget.table.item(i, 0).text())
        assert exp.category == int(widget.table.item(i, 1).text())

        assert exp.expense_date - datetime.strptime(
            widget.table.item(i, 2).text(), "%d.%m.%Y %H:%M"
        ) < timedelta(minutes=1)

        assert exp.added_date - datetime.strptime(
            widget.table.item(i, 3).text(), "%d.%m.%Y %H:%M"
        ) < timedelta(minutes=1)

        assert exp.comment == widget.table.item(i, 4).text()


def test_set_categories(qtbot, cat_repo):
    widget = ExpenseTableBox()

    qtbot.addWidget(widget)

    widget.set_categories(cat_repo.get_all())

    assert {cat.pk: cat.name for cat in cat_repo.get_all()} == widget.cat_dict


def test_set_exp_table_changed_callback(qtbot, get_callback):
    widget = ExpenseTableBox()
    qtbot.addWidget(widget)

    widget.set_exp_table_changed_callback(get_callback)

    assert get_callback == widget.table.cell_changed_callback


def test_cell_changed(qtbot, get_callback, exp_repo):
    widget = ExpenseTableBox()
    qtbot.addWidget(widget)

    widget.set_expenses(exp_repo.get_all())

    widget.table.set_cell_changed_callback(get_callback)
    widget.table.cellChanged.emit(1, 0)

    assert get_callback.val1 == 2
    assert get_callback.val2 == widget.table.col_to_attr[0]
    assert get_callback.val3 == widget.table.item(1, 0).text()


def test_set_expenses_with_categories(qtbot, exp_repo, cat_repo):
    widget = ExpenseTableBox()
    qtbot.addWidget(widget)

    widget.set_categories(cat_repo.get_all())
    widget.set_expenses(exp_repo.get_all())

    for i in range(widget.table.rowCount()):

        assert widget.table.item(i, 1).text() == cat_repo.get(exp_repo.get(i + 1).category).name
