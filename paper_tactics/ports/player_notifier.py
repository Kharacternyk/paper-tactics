from abc import ABC
from abc import abstractmethod

from paper_tactics.entities.game import Game


class PlayerNotifier(ABC):
    @abstractmethod
    def notify(self, player_id: str, game: Game) -> None:
        ...


class PlayerGoneException(Exception):
    pass
