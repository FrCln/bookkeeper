"""
Модель бюджета для расходов
"""
from datetime import datetime, timedelta
from dataclasses import dataclass

from bookkeeper.models.expense import Expense

from bookkeeper.repository.abstract_repository import AbstractRepository


@dataclass
class Budget:
    """
    Бюджет, хранит сумму (total),
    рассчитанную на период времени (period),
    а также сумму (spent), потраченную за этот период.
    """
    period: str
    total: int
    spent: int = 0
    pk: int = 0

    def __post_init__(self) -> None:
        if self.period not in ["day", "week", "month"]:
            raise ValueError(f"Got unknown period: {self.period}")

    def update_with_expenses(self, repo: AbstractRepository['Expense']) -> None:
        """
        Рассчитывает потраченную сумму за период времени
        на основании расходов, находящихся в repo
        """
        expenses = repo.get_all()
        today = datetime.today()

        match self.period:
            case "day":
                self.spent = sum(exp.amount for exp in expenses
                                 if today - exp.expense_date < timedelta(days=1))

            case "week":
                self.spent = sum(exp.amount for exp in expenses
                                 if today - exp.expense_date < timedelta(days=7))

            case "month":
                self.spent = sum(exp.amount for exp in expenses
                                 if today - exp.expense_date < timedelta(days=30))
