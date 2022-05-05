from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Generator, NewType
from uuid import UUID

from dateutil.parser import parse as parse_datetime
from psycopg2.extensions import connection as _connection

from states import State

Chunk = NewType('Chunk', list[tuple[UUID, datetime]])


@dataclass
class Base(metaclass=ABCMeta):
    """Базовый класс для продьюсеров получающих данные из postgres"""

    state: State
    conn: _connection
    chunk_size: int

    @property
    def last_modified(self) -> datetime:
        modified = self.state.retrieve_state(self.__class__.__name__)
        return parse_datetime(modified) if modified else datetime(1, 1, 1, 0, 0, 0, 0)

    @last_modified.setter
    def last_modified(self, modified: datetime):
        self.state.save_state(self.__class__.__name__, modified)

    def produce(self) -> Generator[Chunk, None, None]:
        with self.conn.cursor() as curs:
            curs.execute(self._sql(), (self.last_modified,))

            has_rows = True
            while has_rows:
                rows = curs.fetchmany(self.chunk_size)
                if rows:
                    yield rows
                else:
                    has_rows = False

    @abstractmethod
    def _sql(self) -> str:
        """Возвращает sql-запрос.

        Returns
            str
        """
        pass


class PersonModified(Base):
    """Находит все фильмы, в которых приняли участие персоны, чьи данные изменились с последнего синка."""

    def _sql(self) -> str:
        """Возвращает sql-запрос.

        Returns
            str
        """
        return '''
            SELECT pfw.film_work_id, p.modified FROM content.person p 
            INNER JOIN content.person_film_work pfw ON pfw.person_id = p.id
            WHERE p.modified > %s 
            ORDER BY p.modified DESC
        '''


class GenreModified(Base):
    """Находит все фильмы с жанром, чьи данные изменились с последнего синка."""

    def _sql(self) -> str:
        """Возвращает sql-запрос.

        Returns
            str
        """
        return '''
            SELECT gfw.film_work_id, g.modified FROM content.genre g 
            INNER JOIN content.genre_film_work gfw ON gfw.genre_id = p.id
            WHERE g.modified > %s 
            ORDER BY g.modified DESC
        '''


class FilmworkModified(Base):
    """Находит все фильмы, чьи данные изменились с последнего синка."""

    def _sql(self) -> str:
        """Возвращает sql-запрос.

        Returns
            str
        """
        return '''
            SELECT id, modified FROM content.film_work
            WHERE modified > %s 
            ORDER BY modified DESC
        '''
