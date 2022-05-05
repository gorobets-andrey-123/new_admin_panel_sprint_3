from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from pydantic import BaseModel

import documents
import models


@dataclass
class Base(metaclass=ABCMeta):
    """Базовый класс для преобразователей."""

    @abstractmethod
    def transform(self, items: list[BaseModel]) -> list[BaseModel]:
        """

        :param items:
        :return:
        """
        pass


@dataclass
class ElasticSearchMovie(Base):

    def transform(self, items: list[models.Movie]) -> list[documents.Movie]:
        return [self._map(item) for item in items]

    def _map(self, item: models.Movie) -> documents.Movie:
        return documents.Movie(
            
        )
