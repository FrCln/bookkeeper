"""
Модуль описывает репозиторий, работающий c базой данных через SQLite
"""

import sqlite3
import typing
from typing import Any, Type, Optional, List

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, который представляет собой хранилище для
    хранения и извлечения объектов в базе данных SQLite
    """

    def __init__(self, db_file: str, cls: Type[T]) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = [f for f in cls.__annotations__.keys() if f != 'pk']
        self.cls = cls

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            sql = (f"CREATE TABLE IF NOT EXISTS {self.table_name} "
                   "(pk INTEGER PRIMARY KEY, "
                   + ", ".join(self.fields) + ")"
                   )
            cur.execute(sql)

    def add(self, obj: T) -> int:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            fields = ', '.join(self.fields)
            placeholders = ', '.join(['?'] * len(self.fields))
            values = [getattr(obj, f) for f in self.fields]
            cur.execute(f"SELECT 1 FROM {self.table_name} WHERE pk=?", (obj.pk,))
            if cur.fetchone():
                raise sqlite3.IntegrityError("Duplicate primary key")
            cur.execute(f"INSERT INTO {self.table_name} ({fields}) "
                        f"VALUES ({placeholders})",
                        values)
            obj_id = cur.lastrowid
            if obj.pk is not None:
                obj.pk = typing.cast(int, obj_id)
            return typing.cast(int, obj_id)

    def get(self, pk: int) -> Optional[T]:
        with sqlite3.connect(self.db_file) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {self.table_name} WHERE pk = ?", (pk,))
            row = cur.fetchone()
            if row is None:
                return None
            values = {k: row[k] for k in row.keys()}
            return self.cls(**values)

    def get_all(self, where: dict[str, Any] | None = None) -> List[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            if where is None:
                cur.execute(f"SELECT * FROM {self.table_name}")
            else:
                conditions = ' AND '.join(f"{k} = ?" for k in where.keys())
                values = list(where.values())
                cur.execute(f"SELECT * FROM {self.table_name} WHERE {conditions}", values)
            rows = cur.fetchall()
            objects = []
            for row in rows:
                values = [row[i + 1] for i in range(len(self.fields))]
                obj = self.cls(*values)
                obj.pk = row[0]
                objects.append(obj)
            return objects

    def update(self, obj: T) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            fields = ', '.join(f"{f} = ?" for f in self.fields)
            values = [getattr(obj, f) for f in self.fields]
            values.append(obj.pk)
            cur.execute(f"UPDATE {self.table_name} SET {fields} WHERE pk = ?", values)
            if cur.rowcount == 0:
                raise KeyError(f"No {self.cls.__name__} with pk = {obj.pk} found")

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {self.table_name} WHERE pk = ?", (pk,))
            if cur.rowcount == 0:
                raise ValueError(f"No {self.table_name} with pk = {pk} found")
