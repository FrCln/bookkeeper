"""
Модуль описывает репозиторий, сохраняющий в файл на диске
"""
import datetime
from typing import Any
from inspect import get_annotations
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.abstract_repository import T


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, сохраняющий данные в файл на диске. Работает на основе sqlite3.
    """

    def __init__(self, filename: str, cls: type):
        self.db_filename = filename
        self.cls = cls
        self.table = cls.__name__
        columns = get_annotations(cls)
        columns.pop("pk")
        self.columns = columns.keys()
        self.columns_str = ', '.join(self.columns)

        sql_string = f"CREATE TABLE IF NOT EXISTS {self.table} ( {self.columns_str} )"

        with sqlite3.connect(self.db_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_string)
        connection.close()

    def add(self, obj: T) -> int:

        if not hasattr(obj, "pk"):
            raise ValueError("Object must have 'pk' attribute")

        if obj.pk != 0:
            raise ValueError("Object already has 'pk' value")

        sql_string = f"INSERT INTO {self.table} ( {self.columns_str} ) VALUES " \
                     f"({', '.join(['?'] * len(self.columns))})"

        with sqlite3.connect(self.db_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_string, [getattr(obj, col) for col in self.columns])

        pk = cursor.lastrowid or 0
        obj.pk = pk

        connection.close()

        return pk

    def _create_object(self, pk: int, row: list[str]) -> T:
        obj: T = self.cls(**dict(zip(self.columns, row)))
        for i, an_type in get_annotations(self.cls).items():
            if an_type == datetime.datetime:
                setattr(obj, i, datetime.datetime.fromisoformat(getattr(obj, i)))
        obj.pk = pk
        return obj

    def get(self, pk: int) -> T | None:

        sql_string = f"SELECT * FROM {self.table} WHERE ROWID = ?"
        with sqlite3.connect(self.db_filename) as connection:
            cursor = connection.cursor()
            res = cursor.execute(sql_string, (pk,))

        row = res.fetchone()
        connection.close()

        if row is None:
            return None

        return self._create_object(pk, row)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        if where is None:
            sql_string = f"SELECT ROWID, * FROM {self.table}"
            with sqlite3.connect(self.db_filename) as connection:
                cursor = connection.cursor()
                res = cursor.execute(sql_string)

        else:
            where_part1 = ' AND '.join(
                [f'{i} = ?' for i in where.keys() if where[i] is not None]
            )
            where_part2 = ' AND '.join(
                [f'{i} IS NULL' for i in where.keys() if where[i] is None]
            )
            if where_part1 and where_part2:
                where_part = where_part1 + " AND " + where_part2
            else:
                if where_part1:
                    where_part = where_part1
                else:
                    where_part = where_part2

            sql_string = f"SELECT ROWID, * FROM {self.table} WHERE {where_part}"
            items = [where[i] for i in where.keys() if where[i] is not None]
            with sqlite3.connect(self.db_filename) as connection:
                cursor = connection.cursor()
                res = cursor.execute(sql_string, items)

        rows = res.fetchall()
        connection.close()

        return [self._create_object(row[0], row[1:]) for row in rows]

    def update(self, obj: T) -> None:

        if not hasattr(obj, "pk"):
            raise ValueError("Object must have 'pk' attribute")

        if obj.pk == 0:
            raise ValueError("Can't update object with 'pk' = 0")

        pk = obj.pk
        values_str = ", ".join([f"{i} = ?" for i in self.columns])
        new_values = [getattr(obj, col_name) for col_name in self.columns]
        sql_string = f"UPDATE {self.table} SET {values_str} WHERE ROWID = {pk}"

        with sqlite3.connect(self.db_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_string, new_values)

        connection.close()

    def delete(self, pk: int) -> None:
        sql_string = f"DELETE FROM {self.table} WHERE ROWID = {pk}"
        with sqlite3.connect(self.db_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_string)

        if cursor.rowcount == 0:
            raise ValueError("Deleting object with unknown 'pk'")

        connection.close()

    def clear(self) -> None:
        sql_string = f"DELETE FROM {self.table}"
        with sqlite3.connect(self.db_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_string)

        connection.close()
