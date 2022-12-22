"""
Модель категории расходов
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Generator

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

    def get_all_parents(self, repo: AbstractRepository['Category']) -> Generator['Category', None, None]:
        """
        Generator of all parents in category hierarchy

        Parameters
        ----------
        repo - repository to get objects

        Yields
        -------
        Category objects from direct parent up to root
        """
        parent = self.get_parent(repo)
        if parent is None:
            return
        yield parent
        yield from parent.get_all_parents(repo)

    def get_subcategories(self, repo: AbstractRepository['Category']) \
            -> Generator['Category', None, None]:
        """
        Get all subcategories from whole tree, i.d. self's children,
        their children and so on.

        Parameters
        ----------
        repo - repository to get objects

        Yields
        -------
        Category objects that are successors of self
        """
        def get_children(graph, root):
            """ dfs in graph from root """
            for x in graph[root]:
                yield x
                yield from get_children(graph, x.pk)

        subcats = defaultdict(list)
        for c in repo.get_all():
            subcats[c.parent].append(c)
        return get_children(subcats, self.pk)
