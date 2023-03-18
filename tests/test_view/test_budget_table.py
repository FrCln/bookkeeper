import pytest

from bookkeeper.models.budget import Budget
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.budget_table import BudgetTableBox


@pytest.fixture
def get_callback():
    def callback(val1: str, val2: str, val3: str) -> None:
        callback.val1 = val1
        callback.val2 = val2
        callback.val3 = val3

    return callback


@pytest.fixture
def repo():
    repo = MemoryRepository()
    repo.add(Budget(period="day", total=100))
    repo.add(Budget(period="week", total=500))
    repo.add(Budget(period="month", total=10000))
    return repo


def test_set_budget(qtbot, repo):
    widget = BudgetTableBox()
    qtbot.addWidget(widget)

    widget.set_budget(repo.get_all())

    data = repo.get_all()
    for i in range(widget.table.rowCount()):
        exp: Budget = data[i]

        assert exp.spent == int(widget.table.item(i, 0).text())
        assert exp.total == int(widget.table.item(i, 1).text())


def test_set_exp_table_changed_callback(qtbot, get_callback):
    widget = BudgetTableBox()
    qtbot.addWidget(widget)

    widget.set_budget_table_changed_callback(get_callback)

    assert get_callback == widget.table.cell_changed_callback


def test_cell_changed(qtbot, get_callback, repo):
    widget = BudgetTableBox()
    qtbot.addWidget(widget)

    widget.set_budget(repo.get_all())

    widget.table.set_cell_changed_callback(get_callback)
    widget.table.cellChanged.emit(1, 0)

    assert get_callback.val1 == widget.table.row_to_period[1]
    assert get_callback.val2 == widget.table.col_to_attr[0]
    assert get_callback.val3 == widget.table.item(1, 0).text()
