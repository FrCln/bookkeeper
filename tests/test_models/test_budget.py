from datetime import datetime
from bookkeeper.models.budget import Budget
from bookkeeper.repository.memory_repository import MemoryRepository

import pytest


@pytest.fixture
def repo():
    return MemoryRepository()


class TestBudget:

    def test_create_for_current_month_new_budget(self, repo):
        budget = Budget.create_for_current_month(1000, repo)
        assert budget.term == datetime.now().replace(day=1)
        assert budget.amount == 1000
        assert budget.pk != 0
        assert budget.comment == ''
        assert repo.get(budget.pk) == budget

    def test_create_for_current_month_existing_budget(self, repo):
        existing_budget = Budget(datetime.now().replace(day=1), 500)
        repo.add(existing_budget)
        budget = Budget.create_for_current_month(1000, repo)
        assert budget == existing_budget

    def test_create_for_current_month_with_comment(self, repo):
        budget = Budget.create_for_current_month(1000, repo, comment="test")
        assert budget.term == datetime.now().replace(day=1)
        assert budget.amount == 1000
        assert budget.pk != 0
        assert budget.comment == "test"
        assert repo.get(budget.pk) == budget
