import sqlite3
from dataclasses import dataclass

from psycopg2.extensions import connection as _connection

import models


@dataclass
class SQLiteLoader:
    """Класс для получения данных из sqlite-хранилища."""

    conn: sqlite3.Connection

    def __post_init__(self):
        self.conn.row_factory = sqlite3.Row

    def load_data(self, table_name: str, chunk_size: int) -> models.RawData:
        """Загружает данные из таблицы и возвращает генератор для их перебора чанками.

        Args:
            table_name: str
            chunk_size: int

        Yields:
            models.Data
        """
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM {table} ORDER BY id'.format(table=table_name))

        has_rows = True
        while has_rows:
            rows = cur.fetchmany(chunk_size)
            if rows:
                yield rows
            else:
                has_rows = False

    def total(self, table_name: str) -> int:
        """Возвращает количество записей в таблице.

        Args:
            table_name: str

        Returns:
            int
        """
        sql = 'SELECT COUNT(*) AS total FROM {table} '.format(table=table_name)
        cur = self.conn.cursor()
        cur.execute(sql)

        return cur.fetchone()['total']

    def total_unique(self, table_name: str, unique_columns: tuple) -> int:
        """Возвращает количество уникальных записей в таблице.

        Args:
            table_name: str
            unique_columns: tuple

        Returns:
            int
        """
        sql = 'SELECT COUNT(*) as total FROM (SELECT 1 AS total FROM {table} GROUP BY {columns})'.format(
            table=table_name,
            columns=','.join(unique_columns),
        )

        cur = self.conn.cursor()
        cur.execute(sql)

        return cur.fetchone()['total']


@dataclass
class PostgresLoader:
    """Класс для получения данных из postresql."""

    conn: _connection

    def load_by_ids(self, table_name: str, ids: list) -> models.RawData:
        """Возвращает записи из таблицы по переданному списку айдишников.

        Args:
            table_name: str
            ids: list

        Returns:
            models.Data
        """
        with self.conn.cursor() as cur:
            sql = 'SELECT * FROM {table} WHERE id IN %s ORDER BY id'.format(table=table_name)
            cur.execute(sql, (tuple(ids),))
            return cur.fetchall()

    def total(self, table_name: str) -> int:
        """Возвращает количество записей в таблице.

        Args:
            table_name: str

        Returns:
            int
        """
        with self.conn.cursor() as cur:
            sql = 'SELECT COUNT(*) FROM {table}'.format(table=table_name)
            cur.execute(sql)
            return cur.fetchone()[0]

    def total_unique(self, table_name: str, unique_columns: tuple) -> int:
        """Возвращает количество уникальных записей в таблице.

        Args:
            table_name: str
            unique_columns: tuple

        Returns:
            int
        """
        with self.conn.cursor() as cur:
            sql = 'SELECT COUNT(*) FROM (SELECT 1 AS total FROM {table} GROUP BY {columns}) tmp'.format(
                table=table_name,
                columns=','.join(unique_columns),
            )

            cur.execute(sql)
            return cur.fetchone()[0]
