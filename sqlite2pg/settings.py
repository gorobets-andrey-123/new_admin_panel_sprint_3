import os
import types

from psycopg2.extras import DictCursor, register_uuid

import models

register_uuid()

# Кол-во загружаемых записей за раз
CHUNK_SIZE = 1000

# Загружаемые таблицы и связанные с ними сущности,
# в которые будут отображены полученные из sqlite строки
TABLE_ENTITY_CLS_MAP = types.MappingProxyType({
    'film_work': models.Filmwork,
    'person': models.Person,
    'genre': models.Genre,
    'genre_film_work': models.GenreFilmwork,
    'person_film_work': models.PersonFilmwork,
})

PG_DSL = dict(
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST', '127.0.0.1'),
    port=os.environ.get('DB_PORT', 5432),
    options='-c search_path=public,content',
    cursor_factory=DictCursor,
)
SQLITE_DB_PATH = os.environ.get('SQLITE_PATH', 'db.sqlite')
