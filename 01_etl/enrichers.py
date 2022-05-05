from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from psycopg2.extensions import connection as _connection

import models


@dataclass
class Base(metaclass=ABCMeta):
    conn: _connection

    @abstractmethod
    def enrich(self, ids: list[UUID]) -> list[Any]:
        pass


class Movie(Base):
    def enrich(self, ids: list[UUID]) -> list[models.Movie]:
        with self.conn.cursor() as curs:
            sql = '''
                SELECT
                    fw.id,
                    fw.title,
                    fw.description,
                    fw.rating,
                    COALESCE (
                        json_agg(
                           DISTINCT jsonb_build_object(
                               'id', p.id,
                               'role', pfw.role,
                               'full_name', p.full_name
                           )
                       ) FILTER (WHERE p.id is not null),
                       '[]'
                    ) as persons,
                    array_agg(DISTINCT g.name) as genres
                FROM content.film_work fw
                LEFT JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
                LEFT JOIN genre g on g.id = gfw.genre_id
                LEFT JOIN person_film_work pfw on fw.id = pfw.film_work_id
                LEFT JOIN person p on p.id = pfw.person_id
                WHERE fw.id = ANY(%s)
                GROUP BY fw.id
            '''
            curs.execute(sql, (ids,))
            rows = curs.fetchall()
            return [models.Movie(**row) for row in rows]
