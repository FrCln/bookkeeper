from bookkeeper.repository.sqlite_repository import SQLiteRepository, Test

import pytest




"""@pytest.fixture  
def test_class():
    class Test():
        pk:int = 0
        name: str
        town: str
    
    return Test
   """ 
    
@pytest.fixture()
def repo():
    return SQLiteRepository('test.db', Test)
    
def test_crud(repo):
    obj = Test()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk).name == obj.name
    obj2 = Test("Maria", "London")
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk).name == obj2.name
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo):
    obj = Test()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)

def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)
        
        
def test_cannot_update_without_pk(repo):
    obj = Test()
    with pytest.raises(ValueError):
        repo.update(obj)

def test_get_all(repo):
    objects = [Test() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert len(objects) == len(repo.get_all())
    assert all(repo.get_all()[i].name == objects[i].name for i in range(len(objects)))
    
def test_get_all_with_condition(repo):
    objects = []
    for i in range(5):
        o = Test()
        o.name = str(i)
        o.town = 'test'
        repo.add(o)
        objects.append(o)
    assert len(repo.get_all({'name': '0'})) == 1
    assert repo.get_all({'name': '0'})[0].name == objects[0].name
    print(str(repo.get_all({'town': 'test'})[1].name))
    assert all(repo.get_all({'town': 'test'})[i].name == objects[i].name for i in range(len(objects)))

