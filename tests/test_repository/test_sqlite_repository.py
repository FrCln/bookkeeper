from bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest
import sqlite3
from dataclasses import dataclass

TEST_DB_FILE = "dbfiles/database_test.db"


@pytest.fixture
def clear_db():
    sql_string = "DROP TABLE IF EXISTS Custom"
    with sqlite3.connect(TEST_DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute(sql_string)

    connection.close()


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        value: int
        name: str = None
        pk: int = 0

    return Custom


@pytest.fixture
def repo(custom_class, clear_db):
    return SQLiteRepository(TEST_DB_FILE, custom_class)


def test_crud(repo, custom_class):
    obj = custom_class(name="test_object", value=15)
    pk = repo.add(obj)
    assert pk == obj.pk

    assert repo.get(pk) == obj

    obj2 = custom_class(name="updated_object", value=-35)
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2

    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class(name="test_object", value=15)
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(ValueError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    with pytest.raises(ValueError):
        repo.update(0)


def test_cannot_update_with_zero_pk(repo, custom_class):
    obj = custom_class(name="test", value=5)
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class(value=i, name=f"object{i}") for i in range(5)]
    for o in objects:
        repo.add(o)

    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = [custom_class(value=i, name=f"object") for i in range(5)]
    for obj in objects:
        repo.add(obj)
    assert repo.get_all({'value': 0}) == [objects[0]]
    assert repo.get_all({'name': 'object'}) == objects


def test_get_all_with_none_condition(repo, custom_class):
    objects = [custom_class(value=i) for i in range(5)]
    for obj in objects:
        repo.add(obj)
    assert repo.get_all({'value': 0}) == [objects[0]]
    assert repo.get_all({'name': None}) == objects
    assert repo.get_all({'name': None, 'value': 1}) == [objects[1]]
