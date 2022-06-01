from dataclasses import replace

from paper_tactics.entities.game import Game
from paper_tactics.ports.game_repository import GameRepository, NoSuchGameException


class InMemoryGameRepository(GameRepository):
    def __init__(self) -> None:
        self._games: dict[str, Game] = {}

    def store(self, game: Game) -> None:
        self._games[game.id] = replace(game)

    def fetch(self, game_id: str) -> Game:
        if game_id in self._games:
            return self._games[game_id]
        raise NoSuchGameException(game_id)
