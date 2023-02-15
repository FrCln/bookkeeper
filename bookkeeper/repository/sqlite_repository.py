from itertools import count
from typing import Any
import sqlite3
#import pandas as pd

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
		self.cls = cls
		self.fields = get_annotations(cls, eval_str=True)
		self.fields.pop('pk')
		names = ', '.join(self.fields.keys())
		print('names_in_creation', names)
		with sqlite3.connect(self.db_file) as con:
			cur = con.cursor()
			cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {names});')
		con.commit()
		con.close()


	def add(self, obj: T) -> int:
		names = ', '.join(self.fields.keys())
		p = ', '.join("?" * len(self.fields))
		values = [getattr(obj, x) for x in self.fields]
		print(f"INSERT INTO %s (%s) VALUES (%s)" % (self.table_name, names, p), values)
		with sqlite3.connect(self.db_file) as con:
			cur = con.cursor()
			cur.execute('PRAGMA foreign_keys = ON;')
			cur.execute(f"INSERT INTO {self.table_name} ({names}) VALUES ({p});", values)
			con.commit()
			obj.pk = cur.lastrowid
		con.close()
		return obj.pk
		
	
	def get(self, pk: int) -> T | None:
		#names = ', '.join(self.fields.keys())
		with sqlite3.connect(self.db_file) as con:
			cur = con.cursor()
			print(f"SELECT %s FROM %s WHERE id = %s;" % (names, self.table_name, pk))
			res = cur.execute(f"SELECT * FROM {self.table_name} WHERE id = {pk}")
			attrs = res.fetchall()[0][1:]
		con.close()
		return self.cls(*attrs)

    	
	def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
		"""
		Получить все записи по некоторому условию
		where - условие в виде словаря {'название_поля': значение}
		если условие не задано (по умолчанию), вернуть все записи
		"""
		
		list_of_objs = []
		if where is None:
			with sqlite3.connect(self.db_file) as con:
				cur = con.cursor()
				res = cur.execute(f"SELECT * FROM {self.table_name};")
				attribs = res.fetchall()
			con.close()
			for att in attribs:
				need_attr = att[1:]
				list_of_objs.append(self.cls(*need_attr))
			return list_of_objs
		else:
			with sqlite3.connect(self.db_file) as con:
				cur = con.cursor()
				right_sets = []
				for key, value in where.items():
					res = cur.execute(f"""Select * FROM {self.table_name} 
					WHERE {key} = {value};""")
					attrs = set(res.fetchall())
					right_sets.append(attrs)
			con.close()
			good_objs = list(set.intersection(*right_sets))
			if len(good_objs) == 0:
				return list_of_objs
			else:
				for att in good_objs:
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
				print(f"UPDATE {self.table_name} set {ex_name} = {ex_val} WHERE id == {obj.pk};")
				cur.execute(f"UPDATE {self.table_name} SET {ex_name} = '{ex_val}' WHERE id == {obj.pk};")
		con.commit()
		con.close()
				
		
			
			

    	
	def delete(self, pk: int) -> None:
		""" Удалить запись """
		with sqlite3.connect(self.db_file) as con:
			cur = con.cursor()
			cur.execute(f"DELETE FROM {self.table_name} WHERE id = {pk};")
		con.commit()
		con.close()
  
  
  
        
r = SQLiteRepository('test.db', Test)
o = Test('Hello')
t = Test('Bye')
r.add(o)
r.add(t)
o.name = 'Changed Hello'
r.update(o)
r.delete(2)
#print(r.get(1))
#print(r.get_all({'id': 1}))
#print(o.pk)
#print(t.pk)
