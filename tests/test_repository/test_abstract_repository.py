from bookkeeper.repository.abstract_repository import AbstractRepository

import pytest


def test_cannot_create_abstract_repository():
    with pytest.raises(TypeError):
        AbstractRepository()


def test_can_create_subclass():
    class Test(AbstractRepository):
        def add(self, obj): pass
        def get(self, pk): pass

    t = Test()
    assert isinstance(t, Test)
