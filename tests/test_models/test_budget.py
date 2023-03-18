import pytest

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository


@pytest.fixture
def exp_repo():
    repo = MemoryRepository()
    [repo.add(Expense(amount=i, category=i)) for i in range(1, 6)]
    return MemoryRepository()


def test_create_object():
    b = Budget(period="day", total=15)
    assert b.period == "day"
    assert b.pk == 0
    assert b.total == 15

    b = Budget(period="week", total=15, pk=2, spent=1)
    assert b.period == "week"
    assert b.pk == 2
    assert b.total == 15
    assert b.spent == 1

    with pytest.raises(ValueError):
        Budget(period="year", total=15, pk=2, spent=1)


def test_reassign():
    """
    class should not be frozen
    """
    b = Budget(period="day", total=15)
    b.name = "week"
    b.pk = 1
    assert b.name == "week"
    assert b.pk == 1


def test_eq():
    """
    class should implement __eq__ method
    """
    b1 = Budget(period="day", total=15, pk=2)
    b2 = Budget(period="day", total=15, pk=2)
    assert b1 == b2


def test_update_with_expenses(exp_repo):
    b = Budget(period="day", total=15)
    b.update_with_expenses(exp_repo)

    assert b.spent == sum(exp.amount for exp in exp_repo.get_all())

    b = Budget(period="week", total=20)
    b.update_with_expenses(exp_repo)

    assert b.spent == sum(exp.amount for exp in exp_repo.get_all())

    b = Budget(period="month", total=100)
    b.update_with_expenses(exp_repo)

    assert b.spent == sum(exp.amount for exp in exp_repo.get_all())
