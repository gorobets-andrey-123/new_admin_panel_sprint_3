import types
from dataclasses import dataclass, fields
from typing import Type

from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor

import models


@dataclass
class PostgresSaver:
    """Класс для загрузки данных в postresql."""

    conn: _connection
    table_entity_map: types.MappingProxyType

    def save_data(self, table_name: str, data_to_save: models.RawData):
        """Сохраняет данные в бд в рамках одной транзакции.

        Вставляемые строки сгруппированы в рамках одного sql-запроса размером _CHUNK_SIZE.

        Args:
            table_name: str
            data_to_save: models.RawData
        """
        entity_cls = self.table_entity_map[table_name]

        with self.conn.cursor() as cur:
            for chunk in data_to_save:
                columns, values_sql = self._build_values_sql(cur, entity_cls, chunk)
                sql = f'INSERT INTO {table_name}({columns}) VALUES {values_sql} ON CONFLICT DO NOTHING'
                cur.execute(sql)

    @staticmethod
    def _build_values_sql(cur: cursor, entity_cls: Type[models.Entity], chunk: list[dict]) -> (str, str):
        entity_fields = ()
        values_tmpl = ''
        chunk_values = []

        for row in chunk:
            entity = entity_cls.create_from_sqlite_row(row)

            if not entity_fields:
                entity_fields = fields(entity)
                placeholders_str = ','.join(['%s' for _ in range(len(entity_fields))])
                values_tmpl = '({placeholders})'.format(placeholders=placeholders_str)

            entity_vals = [getattr(entity, field.name) for field in entity_fields]
            row_values = cur.mogrify(values_tmpl, entity_vals).decode('utf-8')
            chunk_values.append(row_values)

        columns = ','.join([field.name for field in entity_fields])
        return columns, ','.join(chunk_values)
