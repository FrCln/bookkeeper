'''Sqlite for working with database'''
import sqlite3
from typing import Any
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T

'''Class for testing with pk field'''
class Test:
    pk: int = 0
    name: str
    town: str
    def __init__(self, name: str = "Ivan", town: str = "Moscow") -> None:
        self.name = name
        self.town = town

class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.cls = cls
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        names = ', '.join(self.fields.keys())
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, {names});''')
        con.commit()
        con.close()

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        places = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON;')
            cur.execute(f"INSERT INTO {self.table_name} ({names}) VALUES ({places});", values)
            con.commit()
            if cur.lastrowid is not None:
                obj.pk = cur.lastrowid
        return obj.pk
    
    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT * FROM {self.table_name} WHERE id = {pk}")
            results = res.fetchall()
            if len(results) < 1:
                return None
            attrs = results[0][1:]
        return self.cls(*attrs)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        list_of_objs = []
        if where is None:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                res = cur.execute(f"SELECT * FROM {self.table_name};")
                attribs = res.fetchall()
            for att in attribs:
                need_attr = att[1:]
                list_of_objs.append(self.cls(*need_attr))
            return list_of_objs
        else:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                right_sets = []
                for key, value in where.items():
                    res = cur.execute(f"""SELECT * FROM {self.table_name} 
                    WHERE {key} = '{value}';""")
                    attrs = set(res.fetchall())
                    right_sets.append(attrs)
                good_objs = list(set.intersection(*right_sets))
                sorted_objs = sorted(good_objs, key = lambda x: x[0])
                if len(sorted_objs) == 0:
                    return list_of_objs
                else:
                    for att in sorted_objs:
                        need_attr = att[1:]
                        list_of_objs.append(self.cls(*need_attr))
                    return list_of_objs
    
    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        if obj.pk == 0:
            raise ValueError("Trying to update object with unknown primary key")
        names = list(self.fields.keys())
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            for i in range(len(values)):
                ex_name = names[i]
                ex_val = values[i]
                cur.execute(f"""UPDATE {self.table_name} SET {ex_name} = '{ex_val}' 
                WHERE id == {obj.pk};""")
        con.commit()
    
    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE id = {pk};")
            number = cur.fetchall()[0][0]
            if number == 0:
                raise KeyError("Cannot delete unexistent row")
            cur.execute(f"DELETE FROM {self.table_name} WHERE id = {pk};")
        con.commit()
        con.close()
        

        
''' 
r = SQLiteRepository('test.db', Test)
o = Test('Ivan', 'Moscow')
t = Test('James', 'London')
r.add(o)
r.add(t)
o.town = "Paris"
r.update(o)
r.delete(2)
print(r.get(1))
print(r.get_all({'id': 1}))
print(o.pk)
print(t.pk)
'''
