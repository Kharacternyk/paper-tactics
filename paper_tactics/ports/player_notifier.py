from abc import ABC, abstractmethod
from dataclasses import asdict
import json

from paper_tactics.entities.game_view import GameView


class PlayerNotifier(ABC):
    def notify(self, player_id: str, game_view: GameView) -> None:
        self.send(player_id, json.dumps(asdict(game_view), default=list))

    def pong(self, player_id: str) -> None:
        self.send(player_id, 'pong')

    @abstractmethod
    def send(self, player_id: str, message: str) -> None:
        ...


class PlayerGoneException(Exception):
    pass
