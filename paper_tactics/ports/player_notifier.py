from abc import ABC, abstractmethod

from paper_tactics.entities.game_view import GameView


class PlayerNotifier(ABC):
    @abstractmethod
    def notify(self, player_id: str, game_view: GameView) -> None:
        ...


class PlayerGoneException(Exception):
    pass
