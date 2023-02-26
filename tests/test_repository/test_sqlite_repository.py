import pytest
import sqlite3
from dataclasses import dataclass

from bookkeeper.repository.sqlite_repository import SQLiteRepository


@pytest.fixture
def test_class():
    @dataclass
    class Test:
        name: str
        pk: int = 0

    return Test


@pytest.fixture
def repo(tmp_path, test_class):
    db_file = tmp_path / 'test.db'
    r = SQLiteRepository(str(db_file), test_class)
    yield r


def test_crud(repo, test_class):
    obj = test_class('Яблоко')
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = test_class('Банан', pk)
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_add_generates_pk(repo, test_class):
    obj = test_class('John')
    pk = repo.add(obj)
    assert obj.pk == pk
    assert pk > 0


def test_add_duplicate_pk_raises_error(repo, test_class):
    obj = test_class('Яблоко')
    pk = repo.add(obj)
    obj2 = test_class('Банан', pk)
    with pytest.raises(sqlite3.IntegrityError):
        repo.add(obj2)


def test_get_returns_none_for_missing_pk(repo, test_class):
    assert repo.get(123) is None


def test_update_fails_with_missing_pk(repo, test_class):
    obj = test_class('Яблоко')
    with pytest.raises(KeyError):
        repo.update(obj)


def test_delete_fails_with_missing_pk(repo, test_class):
    with pytest.raises(Exception):
        repo.delete(123)


def test_get_all_returns_all_objects(repo, test_class):
    obj1 = test_class('Яблоко')
    obj2 = test_class('Банан')
    repo.add(obj1)
    repo.add(obj2)
    objs = repo.get_all()
    assert obj1 in objs
    assert obj2 in objs


def test_get_all_filters_objects(repo, test_class):
    obj1 = test_class('Яблоко', 1)
    obj2 = test_class('Банан', 2)
    obj3 = test_class('Яблоко', 3)
    repo.add(obj1)
    repo.add(obj2)
    repo.add(obj3)
    objs = repo.get_all(where={'name': 'Яблоко'})
    assert obj1 in objs
    assert obj2 not in objs
    assert obj3 in objs
