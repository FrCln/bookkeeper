"""
Модель категории расходов
"""

from dataclasses import dataclass

from ..repository.abstract_repository import AbstractRepository


@dataclass
class Category:
    """
    Категория расходов, хранит название в атрибуте name и ссылку (id) на родителя
    в атрибуте parent.
    У категорий верхнего уровня parent = None
    """
    name: str
    parent: int | None = None
    pk: int | None = None

    def get_parent(self, repo: AbstractRepository['Category']) -> 'Category | None':
        """
        Get parent category

        Parameters
        ----------
        repo - repository to get objects

        Returns
        -------
        Category object or None if there is no parent
        """
        if self.parent is None:
            return None
        return repo.get(self.parent)
