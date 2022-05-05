from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any

import documents
import transformers


@dataclass
class Base(metaclass=ABCMeta):
    """Базовый класс для загрузчиков"""

    @abstractmethod
    def load(self, items: list[Any]):
        """

        :return:
        """
        pass


@dataclass
class ElasticSearchMovie(Base):
    transformer: transformers.ElasticSearchMovie

    def load(self, items: list[Any]):
        for item in items:
            print(item)
        raise Exception()
