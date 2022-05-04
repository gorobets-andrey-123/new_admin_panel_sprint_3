from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Generator, NewType
from uuid import UUID

from dateutil.parser import parse as parse_datetime
from psycopg2.extensions import connection as _connection

from .states import State

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
        return parse_datetime(modified) if modified else datetime(0, 0, 0, 0, 0, 0, 0)

    @last_modified.setter
    def last_modified(self, modified: datetime):
        self.state.save_state(self.__class__.__name__, modified)

    def produce(self) -> Generator[Chunk, None, None]:
        with self.conn.cursor() as curs:
            curs.execute(self._sql(), self.last_modified)

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
            SELECT pfw.filmwork_id, p.modified FROM content.person p 
            INNER JOIN content.person_film_work pfw ON pfw.person_id = p.id
            WHERE p.modified > %s 
            ORDER BY p.modified DESC
        '''


class GenreModified(Base):

    def produce(self) -> Generator[Chunk, None, None]:
        pass


class FilmworkModified(Base):

    def produce(self) -> Generator[Chunk, None, None]:
        pass
