import os

from psycopg2.extras import DictCursor, register_uuid

register_uuid()

# Частота проверки обновлений
CHECK_INTERVAL_SEC = os.environ.get('CHECK_INTERVAL_SEC', 10)

# Кол-во загружаемых записей за раз из бд
CHUNK_SIZE = 1000

PG_DSL = dict(
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST', '127.0.0.1'),
    port=os.environ.get('DB_PORT', 5432),
    options='-c search_path=public,content',
    cursor_factory=DictCursor,
)

REDIS_DSL = dict(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=os.environ.get('REDIS_PORT', 6379),
    db=os.environ.get('REDIS_DB', 0)
)

# ключ, по которому будет храниться состояние в хранилище
STORAGE_STATE_KEY = 'etl'
