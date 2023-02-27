"""
Модель категории расходов
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator

from ..repository.abstract_repository import AbstractRepository


@dataclass
class Category:
    """
    Категория расходов, хранит название в атрибуте name и ссылку (id) на
    родителя (категория, подкатегорией которой является данная) в атрибуте parent.
    У категорий верхнего уровня parent = None
    """
    name: str
    parent: int | None = None
    pk: int = 0

    def get_parent(self,
                   repo: AbstractRepository['Category']) -> 'Category | None':
        """
        Получить родительскую категорию в виде объекта Category
        Если метод вызван у категории верхнего уровня, возвращает None

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Returns
        -------
        Объект класса Category или None
        """
        if self.parent is None:
            return None
        return repo.get(self.parent)

    def get_all_parents(self,
                        repo: AbstractRepository['Category']
                        ) -> Iterator['Category']:
        """
        Получить все категории верхнего уровня в иерархии.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category от родителя и выше до категории верхнего уровня
        """
        parent = self.get_parent(repo)
        if parent is None:
            return
        yield parent
        yield from parent.get_all_parents(repo)

    def get_subcategories(self,
                          repo: AbstractRepository['Category']
                          ) -> Iterator['Category']:
        """
        Получить все подкатегории из иерархии, т.е. непосредственные
        подкатегории данной, все их подкатегории и т.д.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category, являющиеся подкатегориями разного уровня ниже данной.
        """

        def get_children(graph: dict[int | None, list['Category']],
                         root: int) -> Iterator['Category']:
            """ dfs in graph from root """
            for x in graph[root]:
                yield x
                yield from get_children(graph, x.pk)

        subcats = defaultdict(list)
        for cat in repo.get_all():
            subcats[cat.parent].append(cat)
        return get_children(subcats, self.pk)

    @classmethod
    def create_from_tree(
            cls,
            tree: list[tuple[str, str | None]],
            repo: AbstractRepository['Category']) -> list['Category']:
        """
        Создать дерево категорий из списка пар "потомок-родитель".
        Список должен быть топологически отсортирован, т.е. потомки
        не должны встречаться раньше своего родителя.
        Проверка корректности исходных данных не производится.
        При использовании СУБД с проверкой внешних ключей, будет получена
        ошибка (для sqlite3 - IntegrityError). При отсутствии проверки
        со стороны СУБД, результат, возможно, будет корректным, если исходные
        данные корректны за исключением сортировки. Если нет, то нет.
        "Мусор на входе, мусор на выходе".

        Parameters
        ----------
        tree - список пар "потомок-родитель"
        repo - репозиторий для сохранения объектов

        Returns
        -------
        Список созданных объектов Category
        """
        created: dict[str, Category] = {}
        for child, parent in tree:
            # проверяем не существует ли уже категория
            existing_cats = repo.get_all({'name': child})
            if len(existing_cats) > 0:
                created[child] = existing_cats[0]
                continue
            # проверяем существует ли родительская категория
            parent_cats = repo.get_all({'name': parent})
            if len(parent_cats) == 0 and parent is not None:
                raise KeyError(f"Parent category '{parent}' not found")
            parent_cat = parent_cats[0] if parent_cats else None
            cat = cls(child, parent_cat.pk if parent_cat else None)
            repo.add(cat)
            created[child] = cat
        return list(created.values())
