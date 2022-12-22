"""
Модель категории расходов
"""

from dataclasses import dataclass


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
