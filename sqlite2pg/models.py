from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Generator, NewType
from uuid import UUID

from dateutil.parser import parse as parse_datetime

RawData = NewType('Data', Generator[list[dict], None, None])


@dataclass(frozen=True)
class Entity(ABC):
    """Базовый класс для всех загружаемых сущностей."""

    @staticmethod
    @abstractmethod
    def create_from_sqlite_row(row: dict) -> Entity:
        """Метод создания сущности из записи sqlite.

        Args:
            row: dict

        Returns:
            Entity
        """


@dataclass(frozen=True)
class Filmwork(Entity):
    """Сущность кинопроизведения."""

    id: UUID
    title: str
    description: str
    creation_date: datetime.date
    rating: float
    type: str
    created: datetime
    modified: datetime

    @staticmethod
    def create_from_sqlite_row(row: dict) -> Filmwork:
        """Метод создания сущности Filmwork из записи sqlite.

        Args:
            row: dict

        Returns:
            Filmwork
        """
        return Filmwork(
            id=UUID(row['id']),
            title=row['title'],
            description=row['description'] or '',
            creation_date=parse_datetime(row['creation_date']) if row['creation_date'] else None,
            rating=row['rating'] or 0,
            type=row['type'],
            created=parse_datetime(row['created_at']),
            modified=parse_datetime(row['updated_at']),
        )


@dataclass(frozen=True)
class Person(Entity):
    """Сущность актера."""

    id: UUID
    full_name: str
    birth_date: datetime.date
    created: datetime
    modified: datetime

    @staticmethod
    def create_from_sqlite_row(row: dict) -> Person:
        """Метод создания сущности Person из записи sqlite.

        Args:
            row: dict

        Returns:
            Person
        """
        return Person(
            id=UUID(row['id']),
            full_name=row['full_name'],
            birth_date=None,
            created=parse_datetime(row['created_at']),
            modified=parse_datetime(row['updated_at']),
        )


@dataclass(frozen=True)
class PersonFilmwork(Entity):
    """Связь актера с кинопроизведением."""

    id: UUID
    film_work_id: UUID
    person_id: UUID
    role: str
    created: datetime

    @staticmethod
    def create_from_sqlite_row(row: dict) -> PersonFilmwork:
        """Метод создания сущности PersonFilmwork из записи sqlite.

        Args:
            row: dict

        Returns:
            PersonFilmwork
        """
        return PersonFilmwork(
            id=UUID(row['id']),
            film_work_id=UUID(row['film_work_id']),
            person_id=UUID(row['person_id']),
            role=row['role'],
            created=parse_datetime(row['created_at']),
        )


@dataclass(frozen=True)
class Genre(Entity):
    """Жанры."""

    id: UUID
    name: str
    description: str
    created: datetime
    modified: datetime

    @staticmethod
    def create_from_sqlite_row(row: dict) -> Genre:
        """Метод создания сущности PersonFilmwork из записи sqlite.

        Args:
            row: dict

        Returns:
            Genre
        """
        return Genre(
            id=UUID(row['id']),
            name=row['name'],
            description=row['description'] or '',
            created=parse_datetime(row['created_at']),
            modified=parse_datetime(row['updated_at']),
        )


@dataclass(frozen=True)
class GenreFilmwork(Entity):
    """Связь жанра с кинопроизведением."""

    id: UUID
    film_work_id: UUID
    genre_id: UUID
    created: datetime

    @staticmethod
    def create_from_sqlite_row(row: dict) -> GenreFilmwork:
        """Метод создания сущности GenreFilmwork из записи sqlite.

        Args:
            row: dict

        Returns:
            GenreFilmwork
        """
        return GenreFilmwork(
            id=UUID(row['id']),
            film_work_id=UUID(row['film_work_id']),
            genre_id=UUID(row['genre_id']),
            created=parse_datetime(row['created_at']),
        )
