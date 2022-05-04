from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import redis


@dataclass
class BaseStorage(metaclass=ABCMeta):
    """Базовый класс для храненеия состояний etl."""

    @abstractmethod
    def retrieve_state(self) -> dict:
        """Возвращает сохраненное состояние.

        Returns:
            dict
        """
        pass

    @abstractmethod
    def save_state(self, state: dict) -> bool:
        """Сохраняет состояние.

        Args:
            state: dict

        Returns:
            Any
        """
        pass


@dataclass
class RedisStorage(BaseStorage):
    redis: redis.Redis
    key: str

    def retrieve_state(self) -> Any:
        """Возвращает сохраненное состояние.

        Returns:
            dict
        """
        return self.redis.hgetall(self.key)

    def save_state(self, state: dict) -> None:
        """Сохраняет состояние.

        Args:
            state: dict

        Returns:
            Any
        """
        self.redis.hset(self.key, mapping=state)


@dataclass
class State:
    storage: BaseStorage
    _state: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self._state = self.storage.retrieve_state()

    def retrieve_state(self, key: str) -> Any:
        """Возвращает сохраненное состояние по ключу.

        Args:
            key: str

        Returns:
            Any
        """
        return self._state.get(key)

    def save_state(self, key: str, value: Any) -> bool:
        """Сохраняет значение по ключу.

        Args:
            key: str
            value: Any

        Returns:
            bool
        """
        self._state[key] = value
        return self.storage.save_state(self._state)
