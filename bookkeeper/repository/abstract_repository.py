"""
Модуль содержит описание абстрактного репозитория
"""

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    """
    Абстрактный репозиторий.
    Абстрактные методы:
    add
    get
    """

    @abstractmethod
    def add(self, obj) -> int:
        """ Добавить объект в репозиторий, вернуть id объекта """

    @abstractmethod
    def get(self, pk):
        """ Получить объект по id """
