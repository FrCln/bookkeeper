"""
Модель категории бюджета
"""
from dataclasses import dataclass, field
from datetime import datetime
from bookkeeper.repository.abstract_repository import AbstractRepository


@dataclass(slots=True)
class Budget:
    """
    term - объект datetime, представляющий месяц, на который действителен бюджет
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    term: datetime
    amount: float
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0

    @classmethod
    def create_for_current_month(cls, amount: float, repo: AbstractRepository['Budget'], comment: str = '')\
            -> 'Budget':
        """
        Создать бюджет для текущего месяца, если его еще нет.

        Parameters
        ----------
        amount - сумма бюджета на месяц
        repo - репозиторий для сохранения объектов

        Returns
        -------
        Созданный объект Budget
        """
        term = datetime.now().replace(day=1)
        existing_budgets = repo.get_all({'term': term})
        if existing_budgets:
            return existing_budgets[0]
        budget = cls(term, amount, comment=comment)
        repo.add(budget)
        return budget
