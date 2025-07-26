from typing import Optional
from uuid import uuid4

from paper_tactics.entities.game import Game
from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.entities.player import Player
from paper_tactics.ports.game_repository import GameRepository
from paper_tactics.ports.logger import Logger
from paper_tactics.ports.match_request_queue import MatchRequestQueue
from paper_tactics.ports.player_notifier import PlayerNotifier
from paper_tactics.use_cases.notify_player import (
    notify_active_player,
    notify_passive_player,
)


def create_game(
    game_repository: GameRepository,
    match_request_queue: MatchRequestQueue,
    player_notifier: PlayerNotifier,
    logger: Logger,
    request: MatchRequest,
) -> None:
    if request.game_preferences and not request.game_preferences.valid:
        return

    queued_request: Optional[MatchRequest]

    if request.game_preferences and request.game_preferences.is_against_bot:
        queued_request = request
        request = MatchRequest(game_preferences=request.game_preferences)
    else:
        while True:
            queued_request = match_request_queue.pop(request.game_preferences)

            if not queued_request:
                match_request_queue.put(request)
                return

            if queued_request.id != request.id:
                break

    active_player = Player(id=queued_request.id, view_data=queued_request.view_data)
    passive_player = Player(id=request.id, view_data=request.view_data)

    preferences = request.game_preferences
    if not preferences:
        preferences = queued_request.game_preferences
        if not preferences:
            preferences = GamePreferences()

    game = Game(
        id=uuid4().hex,
        active_player=active_player,
        passive_player=passive_player,
        preferences=preferences,
    )

    game.init()

    if not notify_active_player(player_notifier, game, logger):
        return match_request_queue.put(request)

    if notify_passive_player(player_notifier, game, logger):
        game_repository.store(game)
