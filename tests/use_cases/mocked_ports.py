from dataclasses import replace
from typing import Iterable, Optional

from paper_tactics.entities.game import Game
from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.ports.game_repository import GameRepository, NoSuchGameException
from paper_tactics.ports.logger import Logger
from paper_tactics.ports.match_request_queue import MatchRequestQueue
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


class MockedMatchRequestQueue(MatchRequestQueue):
    def __init__(self, requests: Optional[Iterable[MatchRequest]]):
        self.requests: list = list(requests) if requests is not None else []

    def put(self, request: MatchRequest) -> None:
        self.requests.append(request)

    def pop(self, preferences: GamePreferences) -> Optional[MatchRequest]:
        queued_request = next(
            (
                request
                for request in self.requests
                if request.game_preferences == preferences
            ),
            None,
        )
        if queued_request:
            self.requests.remove(queued_request)
        return queued_request


class MockedPlayerNotifier(PlayerNotifier):
    def __init__(self, active_player_is_gone: bool, passive_player_is_gone: bool):
        self.active_player_is_gone = active_player_is_gone
        self.passive_player_is_gone = passive_player_is_gone
        self.notified_player_ids: list[str] = []

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
