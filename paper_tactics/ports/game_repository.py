from abc import ABC, abstractmethod

from paper_tactics.entities.game import Game


class GameRepository(ABC):
    @abstractmethod
    def store(self, game: Game) -> None:
        ...

    @abstractmethod
    def fetch(self, game_id: str) -> Game:
        ...


class NoSuchGameException(Exception):
    pass
