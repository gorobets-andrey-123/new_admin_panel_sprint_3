from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class RoleEnum(str, Enum):
    actor = 'actor'
    writer = 'writer'
    director = 'director'


class Actor(BaseModel):
    id: UUID
    role: RoleEnum =
    full_name: str


class Movie(BaseModel):
    id: UUID
    title: str
    description: str
    imdb_rating: float
    genre: list[str]
    actor_names: list[str]
    actors: list[Person]
