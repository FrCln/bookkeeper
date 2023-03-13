"""
Модель категории бюджета
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
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
    period: str = "month"

    @classmethod
    def create_for_current_month(cls, amount: float,
                                 repo: AbstractRepository['Budget'], comment: str = '')\
            -> 'Budget':
        """
        Создать бюджет для текущего месяца, если его еще нет.

        Parameters
        ----------
        amount - сумма бюджета на месяц
        repo - репозиторий для сохранения объектов
        period - на месяц

        Returns
        -------
        Созданный объект Budget
        """
        term = datetime.now().replace(day=1)
        existing_budgets = repo.get_all({'term': term, 'period': 'month'})
        if existing_budgets:
            return existing_budgets[0]
        budget = cls(term, amount, comment=comment, period='month')
        repo.add(budget)
        return budget

    @classmethod
    def create_for_current_week(cls, amount: float,
                                repo: AbstractRepository['Budget'], comment: str = '') \
            -> 'Budget':
        """
        Создать бюджет для текущей недели, если его еще нет.

        Parameters
        ----------
        amount - сумма бюджета на неделю
        repo - репозиторий для сохранения объектов
        period - на неделю

        Returns
        -------
        Созданный объект Budget
        """
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        existing_budgets = repo.get_all({'term': week_start, 'period': 'week'})
        if existing_budgets:
            return existing_budgets[0]
        budget = cls(week_start, amount, comment=comment, period='week')
        repo.add(budget)
        return budget

    @classmethod
    def create_for_current_day(cls, amount: float,
                               repo: AbstractRepository['Budget'], comment: str = '') \
            -> 'Budget':
        """
        Создать бюджет для текущего дня, если его еще нет.

        Parameters
        ----------
        amount - сумма бюджета на день
        repo - репозиторий для сохранения объектов
        period - на день

        Returns
        -------
        Созданный объект Budget
        """
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        existing_budgets = repo.get_all({'term': today, 'period': 'day'})
        if existing_budgets:
            return existing_budgets[0]
        budget = cls(today, amount, comment=comment, period='day')
        repo.add(budget)
        return budget
