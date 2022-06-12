from uuid import uuid4

from paper_tactics.entities.game import Game
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.entities.player import Player
from paper_tactics.ports.game_repository import GameRepository
from paper_tactics.ports.logger import Logger
from paper_tactics.ports.match_request_queue import MatchRequestQueue
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


def create_game(
    game_repository: GameRepository,
    match_request_queue: MatchRequestQueue,
    player_notifier: PlayerNotifier,
    logger: Logger,
    request: MatchRequest,
) -> None:
    if not request.game_preferences.valid:
        return

    queued_request = match_request_queue.pop(request.game_preferences)

    if not queued_request or queued_request.id == request.id:
        match_request_queue.put(request)
        return

    active_player = Player(id=queued_request.id, view_data=queued_request.view_data)
    passive_player = Player(id=request.id, view_data=request.view_data)
    game = Game(
        id=uuid4().hex,
        active_player=active_player,
        passive_player=passive_player,
        preferences=request.game_preferences,
    )

    game.init_players()

    try:
        player_notifier.notify(queued_request.id, game)
    except PlayerGoneException as e:
        match_request_queue.put(request)
        return logger.log_exception(e)

    try:
        player_notifier.notify(request.id, game)
    except PlayerGoneException as e:
        return logger.log_exception(e)

    game_repository.store(game)
