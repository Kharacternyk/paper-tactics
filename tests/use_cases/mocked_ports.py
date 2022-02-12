from dataclasses import replace
from typing import Optional

from paper_tactics.entities.game import Game
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.ports.game_repository import GameRepository
from paper_tactics.ports.game_repository import NoSuchGameException
from paper_tactics.ports.logger import Logger
from paper_tactics.ports.match_request_queue import MatchRequestQueue
from paper_tactics.ports.player_notifier import PlayerGoneException
from paper_tactics.ports.player_notifier import PlayerNotifier


class MockedMatchRequestQueue(MatchRequestQueue):
    def __init__(self, request=Optional[MatchRequest]):
        self.request = request

    def put(self, request=Optional[MatchRequest]) -> None:
        assert self.request is None
        self.request = request

    def pop(self) -> Optional[MatchRequest]:
        result = self.request
        self.request = None
        return result


class MockedPlayerNotifier(PlayerNotifier):
    def __init__(self, active_player_is_gone: bool, passive_player_is_gone: bool):
        self.active_player_is_gone = active_player_is_gone
        self.passive_player_is_gone = passive_player_is_gone
        self.notified_player_ids = []

    def notify(self, player_id: str, game: Game) -> None:
        self.notified_player_ids.append(player_id)
        if (
            self.active_player_is_gone
            and game.active_player.id == player_id
            or self.passive_player_is_gone
            and game.passive_player.id == player_id
        ):
            raise PlayerGoneException(player_id)


class MockedGameRepository(GameRepository):
    def __init__(self, stored_games: Optional[dict[str, Game]] = None):
        self.stored_games = stored_games or {}

    def store(self, game: Game) -> None:
        self.stored_games[game.id] = replace(game)

    def fetch(self, game_id: str) -> Game:
        if game_id in self.stored_games:
            return self.stored_games[game_id]
        raise NoSuchGameException(game_id)


class MockedLogger(Logger):
    def __init__(self):
        self.log = []

    def log_exception(self, exception: Exception) -> None:
        self.log.append(exception)
