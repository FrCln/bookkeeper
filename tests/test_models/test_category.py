"""
Тесты для категорий расходов
"""
from inspect import isgenerator

import pytest

from bookkeeper.models.category import Category
from bookkeeper.repository.memory_repository import MemoryRepository


@pytest.fixture
def repo():
    return MemoryRepository()


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


def test_get_parent(repo):
    c1 = Category(name='parent')
    pk = repo.add(c1)
    c2 = Category(name='name', parent=pk)
    repo.add(c2)
    assert c2.get_parent(repo) == c1


def test_get_all_parents(repo):
    parent_pk = None
    for i in range(5):
        c = Category(str(i), parent=parent_pk)
        parent_pk = repo.add(c)
    gen = c.get_all_parents(repo)
    assert isgenerator(gen)
    assert [c.name for c in gen] == ['3', '2', '1', '0']


def test_get_subcategories(repo: MemoryRepository[Category]):
    parent_pk = None
    for i in range(5):
        c = Category(str(i), parent=parent_pk)
        parent_pk = repo.add(c)
    c = repo.get_all({'name': '0'})[0]
    gen = c.get_subcategories(repo)
    assert isgenerator(gen)
    # using set because order doesn't matter
    assert {c.name for c in gen} == {'1', '2', '3', '4'}


def test_get_subcategories_complicated(repo: MemoryRepository[Category]):
    root = Category('0')
    root_pk = repo.add(root)
    repo.add(Category('1', root_pk))
    pk2 = repo.add(Category('2', root_pk))
    repo.add(Category('3', pk2))
    repo.add(Category('4', pk2))

    gen = root.get_subcategories(repo)
    assert isgenerator(gen)
    # using set because order doesn't matter
    assert {c.name for c in gen} == {'1', '2', '3', '4'}


def test_create_from_tree(repo):
    tree = [('parent', None), ('1', 'parent'), ('2', '1')]
    cats = Category.create_from_tree(tree, repo)
    assert len(cats) == len(tree)
    parent = next(c for c in cats if c.name == 'parent')
    assert parent.parent is None
    c1 = next(c for c in cats if c.name == '1')
    assert c1.parent == parent.pk
    c2 = next(c for c in cats if c.name == '2')
    assert c2.parent == c1.pk


def test_create_from_tree_error(repo):
    tree = [('1', 'parent'), ('parent', None)]
    with pytest.raises(KeyError):
        Category.create_from_tree(tree, repo)
