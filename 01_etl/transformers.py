from dataclasses import dataclass
from typing import Any

from . import transformers


@dataclass
class Base:
    def transform(self, items: list[Any]) -> list[Any]:
        pass


@dataclass
class ElasticSearchMovie(Base):

    def transform(self, items: list[Any]) -> list[Any]:
        pass
