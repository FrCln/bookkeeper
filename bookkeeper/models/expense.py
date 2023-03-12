"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: float = 0.0
    category: int = 0
    expense_date: datetime = datetime.now()
    added_date: datetime = datetime.now()
    comment: str = ''
    pk: int = 0
