"""
Модуль описывает репозиторий, работающий с sqlite
"""

import sqlite3
from typing import Any
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T


def gettype(attr: Any) -> str:
    """_summary_

    Args:
        attr (Any): _description_

    Returns:
        str: _description_
    """
    if isinstance(attr, int):
        return 'INTEGER'
    return 'TEXT'


def adddecor(value: str | int) -> str | int:
    """_summary_

    Args:
        attr (Any): _description_

    Returns:
        str | int: _description_
    """
    if isinstance(value, str):
        return f'\'{value}\''
    return value


class SQLiteRepository(AbstractRepository[T]):
    """_summary_

    Args:
        AbstractRepository (_type_): _description_
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.cls_ty = cls

        with sqlite3.connect(self.db_file) as con:
            values = [(f'{x}', gettype(getattr(cls, x))) for x in self.fields]
            qstring = ', '.join([f'{x} {ty}' for x, ty in values])
            cur = con.cursor()
            query = (f'CREATE TABLE IF NOT EXISTS {self.table_name} '
                     f'(id INTEGER PRIMARY KEY, {qstring})')
            cur.execute(query)
        con.close()

    def is_pk_in_db(self, cur: Any, pk: int) -> bool:
        """Forms query to DB to check is records with pk exists.

        Args:
            cur (Any): cursor for query
            pk (int): private key to check

        Returns:
            bool: True if record exists, overwise False
        """
        query = f'SELECT * FROM {self.table_name} WHERE id = {pk}'
        res = cur.execute(query).fetchone()
        return res is not None

    def add(self, obj: T) -> int:
        """Creates record about new object in DB.

        Args:
            obj (T): Object to create record about.

        Raises:
            ValueError: Trying to add  object without pk.
            ValueError: Error while DB processing

        Returns:
            int: private key of inserted record.
        """
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        qmarks = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({qmarks})',
                values
            )
            if not cur.lastrowid:
                raise ValueError("No assignable pk")
            obj.pk = int(cur.lastrowid)

        con.close()
        return obj.pk

    def fill_object(self, result: Any) -> T:
        """Fills attributes of object in accordance with results

        Args:
            result (Any): result of DB query.

        Returns:
            T: Filled object.
        """
        obj: T = self.cls_ty()
        obj.pk = result[0]
        for x, res in zip(self.fields, result[1:]):
            setattr(obj, x, res)
        return obj

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            query = f'SELECT * FROM {self.table_name} WHERE id = {pk}'
            result = con.cursor().execute(query).fetchone()
            if result is None:
                return None
            obj: T = self.fill_object(result)
        con.close()
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию пусто), вернуть все записи
        """
        query = f'SELECT * FROM {self.table_name}'

        condition = ''
        if where is not None:
            condition = ' WHERE'
            for key, val in where.items():
                condition += f' {key} = {adddecor(val)} AND'
            query += condition.rsplit(' ', 1)[0]

        with sqlite3.connect(self.db_file) as con:
            results = con.cursor().execute(query).fetchall()
            objs = [self.fill_object(result) for result in results]

        con.close()
        return objs

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        values = [adddecor(getattr(obj, x)) for x in self.fields]
        setter = [f'{col} = {val}' for col, val in zip(self.fields, values)]
        upd_stm = ', '.join(setter)

        with sqlite3.connect(self.db_file) as con:
            if not self.is_pk_in_db(con.cursor(), obj.pk):
                raise ValueError(f'No object with id={obj.pk} in DB.')
            query = f'UPDATE {self.table_name} SET {upd_stm} WHERE id = {obj.pk}'
            con.cursor().execute(query)
        con.close()

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            if not self.is_pk_in_db(con.cursor(), pk):
                raise KeyError(f'No object with id={pk} in DB.')
            query = f'DELETE FROM {self.table_name} WHERE id = {pk}'
            con.cursor().execute(query)
        con.close()

    def delete_all(self) -> None:
        """Deletes all records in DB.
        """
        with sqlite3.connect(self.db_file) as con:
            query = f'DELETE FROM {self.table_name}'
            con.cursor().execute(query)
        con.close()
