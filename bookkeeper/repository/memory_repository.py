"""
Модуль описывает репозиторий, работающий в оперативной памяти
"""

from itertools import count

from bookkeeper.repository.abstract_repository import AbstractRepository


class MemoryRepository(AbstractRepository):
    """
    Репозиторий, работающий в оперативной памяти. Хранит данные в словаре.
    """

    def __init__(self):
        self._container = {}
        self._counter = count(1)

    def add(self, obj) -> int:
        if getattr(obj, 'pk', ...) is not None:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        pk = next(self._counter)
        self._container[pk] = obj
        obj.pk = pk
        return pk

    def get(self, pk):
        return self._container.get(pk)

    def update(self, obj):
        self._container[obj.pk] = obj

    def delete(self, pk):
        self._container.pop(pk)
