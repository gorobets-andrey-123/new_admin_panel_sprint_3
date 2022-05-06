import logging
import os
import sqlite3
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

import emoji
import psycopg2
from psycopg2.extensions import connection as _connection
from python_log_indenter import IndentedLoggerAdapter

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__)),
    ),
)

import loaders
import models
import settings
import sqlite_funcs

logging.basicConfig(level=logging.INFO, format='%(message)s')


@dataclass(frozen=True)
class Checker(ABC):
    """Базовый класс для всех проверок."""

    sqlite_loader: loaders.SQLiteLoader
    postgres_loader: loaders.PostgresLoader
    log: IndentedLoggerAdapter

    @abstractmethod
    def check(self, table_name: str, entity_cls: Type[models.Entity]):
        """Абстрактный метод, реализуемый в наследниках.

        Args:
            table_name: str
            entity_cls: Type[models.Entity]
        """


@dataclass(frozen=True)
class TotalCheck(Checker):
    """Проверка на соответсвие кол-ва записей в таблицах."""

    def check(self, table_name: str, entity_cls: Type[models.Entity]):
        """Функция запускает проверку.

        Args:
            table_name: str
            entity_cls: Type[models.Entity]
        """
        sqlite_total = self.sqlite_loader.total(table_name)
        postgres_total = self.postgres_loader.total(table_name)

        try:
            assert sqlite_total == postgres_total, emoji.emojize(
                ':cross_mark: Количество записей загруженных в postgres не соответсвует sqlite',
            )
        except Exception as err:
            self.log.error(str(err))
            self.log.add()
            self.log.info('Записей в таблице sqlite: {total}'.format(total=sqlite_total))
            self.log.info('Записей в таблице postgres: {total}'.format(total=postgres_total))
            self.log.sub()
        else:
            self.log.info(emoji.emojize(':check_mark_button: Проверка TotalValuesDiffCheck пройдена'))


@dataclass(frozen=True)
class DataDiffCheck(Checker):
    """Проверка на наличие всех фильмов в postgres."""

    chunk_size: int

    def check(self, table_name: str, entity_cls: Type[models.Entity]):
        """Функция запускает проверку.

        Args:
            table_name: str
            entity_cls: Type[models.Entity]
        """
        loaded_data = self.sqlite_loader.load_data(table_name, self.chunk_size)
        try:
            for chunk in loaded_data:
                ids = [row['id'] for row in chunk]
                sqlite_entities = {entity_cls.create_from_sqlite_row(row) for row in chunk}
                pg_rows = self.postgres_loader.load_by_ids(table_name, ids)
                pg_entities = {entity_cls(**row) for row in pg_rows}

                assert pg_entities == sqlite_entities, emoji.emojize(
                    ':cross_mark: Данные в sqlite отличаются от данных в postgresql',
                )
        except Exception as err:
            self.log.error(str(err))
        else:
            self.log.info(emoji.emojize(':check_mark_button: Проверка PostgresDataDiffCheck пройдена'))


@dataclass(frozen=True)
class TotalUniqueCheck(Checker):
    """Проверка на соответсвие кол-ва уникальных записей в таблице связей актеров и фильмов."""

    unique_columns: tuple

    def check(self, table_name: str, entity_cls: Type[models.Entity]):
        """Функция запускает проверку.

        Args:
            table_name: str
            entity_cls: Type[models.Entity]
        """
        sqlite_total = self.sqlite_loader.total_unique(table_name, self.unique_columns)
        postgres_total = self.postgres_loader.total_unique(table_name, self.unique_columns)

        try:
            assert sqlite_total == postgres_total, emoji.emojize(
                ':cross_mark: Количество уникальных записей загруженных в postgres не соответсвует sqlite',
            )
        except Exception as err:
            self.log.error(str(err))
            self.log.add()
            self.log.info('Уникальных записей в таблице sqlite: {total}'.format(total=sqlite_total))
            self.log.info('Уникальных записей в таблице postgres: {total}'.format(total=postgres_total))
            self.log.sub()
        else:
            self.log.info(emoji.emojize(':check_mark_button: Проверка TotalUniqueCheck пройдена'))


def check_consistency(sqlite_conn: sqlite3.Connection, pg_conn: _connection, table_entity_map: dict, chunk_size: int):
    """Основной метод загрузки данных из SQLite в Postgres.

    Args:
        sqlite_conn: sqlite3.Connection
        pg_conn: _connection
        table_entity_map: dict
        chunk_size: int
    """
    log = IndentedLoggerAdapter(logging.getLogger(__name__))
    sqlite_loader = loaders.SQLiteLoader(sqlite_conn)
    postgres_loader = loaders.PostgresLoader(pg_conn)

    checkers = {
        'film_work': [
            TotalCheck(sqlite_loader, postgres_loader, log),
            DataDiffCheck(sqlite_loader, postgres_loader, log, chunk_size),
        ],
        'person': [
            TotalCheck(sqlite_loader, postgres_loader, log),
            DataDiffCheck(sqlite_loader, postgres_loader, log, chunk_size),
        ],
        'genre': [
            TotalCheck(sqlite_loader, postgres_loader, log),
            DataDiffCheck(sqlite_loader, postgres_loader, log, chunk_size),
        ],
        'genre_film_work': [
            TotalCheck(sqlite_loader, postgres_loader, log),
            DataDiffCheck(sqlite_loader, postgres_loader, log, chunk_size),
        ],
        'person_film_work': [
            TotalUniqueCheck(sqlite_loader, postgres_loader, log, unique_columns=('film_work_id', 'person_id')),
        ],
    }

    for table_name, entity_cls in table_entity_map.items():
        log.info(emoji.emojize('Проверка целостности данных таблицы "{table}"'.format(table=table_name)))
        log.add()

        for checker in checkers[table_name]:
            checker.check(table_name, entity_cls)

        log.sub()


if __name__ == '__main__':
    with sqlite_funcs.conn_context(settings.SQLITE_DB_PATH) as sqlite_conn:
        with psycopg2.connect(**settings.PG_DSL) as pg_conn:
            check_consistency(sqlite_conn, pg_conn, settings.TABLE_ENTITY_CLS_MAP, settings.CHUNK_SIZE)
