from abc import ABC
from abc import abstractmethod
from typing import Optional


class PlayerQueue(ABC):
    @abstractmethod
    def put(self, player_id: str) -> None:
        ...

    @abstractmethod
    def pop(self) -> Optional[str]:
        ...
