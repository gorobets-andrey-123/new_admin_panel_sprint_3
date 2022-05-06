import logging
import sqlite3
import types

import psycopg2
from psycopg2.extensions import connection as _connection

import loaders
import savers
import settings
import sqlite_funcs


def load_from_sqlite(connection: sqlite3.Connection,
                     pg_conn: _connection,
                     table_entity_map: types.MappingProxyType,
                     chunk_size: int,
                     ):
    """Основной метод загрузки данных из SQLite в Postgres.

    Args:
        connection: sqlite3.Connection,
        pg_conn: _connection,
        table_entity_map: types.MappingProxyType,
        chunk_size: int
    """
    sqlite_loader = loaders.SQLiteLoader(connection)
    postgres_saver = savers.PostgresSaver(pg_conn, table_entity_map)

    try:
        for table_name in table_entity_map:
            data_to_save = sqlite_loader.load_data(table_name, chunk_size)
            postgres_saver.save_data(table_name, data_to_save)
    except Exception as err:
        logging.exception(err)


if __name__ == '__main__':
    with sqlite_funcs.conn_context(settings.SQLITE_DB_PATH) as sqlite_conn:
        with psycopg2.connect(**settings.PG_DSL) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn, settings.TABLE_ENTITY_CLS_MAP, settings.CHUNK_SIZE)
