from itertools import count
from typing import Any
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository, T

from inspect import get_annotations

class Test:
	pk: int
	name: str
	
	def __init__(self, name: str) -> None:
		self.name = name
		
print(get_annotations(Test, eval_str = True))


class SQLiteRepository(AbstractRepository[T]):
	def __init__(self, db_file: str, cls: type) -> None:
		self.db_file = db_file
		self.table_name = cls.__name__.lower()
		self.fields = get_annotations(cls, eval_str=True)
		self.fields.pop('pk')
		names = ', '.join(self.fields.keys())
		print('names_in_creation', names)
		with sqlite3.connect(self.db_file) as con:
			cur = con.cursor()
			cur.execute(f'CREATE TABLE %s (%s)' % (self.table_name, names))
		con.close()


	def add(self, obj: T) -> int:
		names = ', '.join(self.fields.keys())
		print("names", names)
		p = ', '.join("?" * len(self.fields))
		print("p", p)
		values = [getattr(obj, x) for x in self.fields]
		print(values)
		with sqlite3.connect(self.db_file) as con:
			cur = con.cursor()
			cur.execute('PRAGMA foreign_keys = ON')
			cur.execute(f"INSERT INTO %s (%s) VALUES (%s)" % (self.table_name, names, p), values)
			#cur.execute(f"INSERT INTO \"{self.table_name}\" (\"{names}\") VALUES (\"{p}\")", values)
			obj.pk = cur.lastrowid
		con.close()
		return obj.pk
		

	def get(self, pk: int) -> T | None:
		""" Получить объект по id """
		pass

    	
	def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
		"""
		Получить все записи по некоторому условию
		where - условие в виде словаря {'название_поля': значение}
		если условие не задано (по умолчанию), вернуть все записи
		"""
		pass

	def update(self, obj: T) -> None:
		""" Обновить данные об объекте. Объект должен содержать поле pk. """
		pass

    	
	def delete(self, pk: int) -> None:
		""" Удалить запись """
		pass
        
r = SQLiteRepository('test.sqlite', Test)
o = Test('Hello')
t = Test('Bye')
r.add(o)
r.add(t)
print(o.pk)
