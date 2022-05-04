from uuid import UUID

from . import models


class Base:

    def enrich(self, ids: list[UUID]) -> list[models.Movie]:
        pass


class Movie(Base):
    pass
