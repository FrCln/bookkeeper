"""
Тесты для категорий расходов
"""

import pytest

from bookkeeper.models.category import Category


def test_create_object():
    c = Category('name')
    assert c.name == 'name'
    assert c.pk is None
    assert c.parent is None

    c = Category(name='name', parent=1, pk=2)
    assert c.name == 'name'
    assert c.parent == 1
    assert c.pk == 2


def test_reassign():
    """
    class should not be frozen
    """
    c = Category('name')
    c.name = 'test'
    c.pk = 1
    assert c.name == 'test'
    assert c.pk == 1


def test_eq():
    """
    class should implement __eq__ method
    """
    c1 = Category(name='name', parent=1, pk=2)
    c2 = Category(name='name', parent=1, pk=2)
    assert c1 == c2
