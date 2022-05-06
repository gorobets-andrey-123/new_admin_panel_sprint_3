import psycopg2
from psycopg2.extensions import connection as _connection

import settings


def truncate_tables(conn: _connection, tables: tuple):
    """Очищает таблицу postgres.

    Args:
        conn: _connection
        tables: tuple
    """
    with conn.cursor() as cur:
        for table in tables:
            cur.execute('TRUNCATE content.{table} CASCADE'.format(table=table))


if __name__ == '__main__':
    with psycopg2.connect(**settings.PG_DSL) as conn:
        truncate_tables(conn, tuple(settings.TABLE_ENTITY_CLS_MAP.keys()))
