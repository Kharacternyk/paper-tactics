from typing import Optional

from paper_tactics.ports.game_repository import GameRepository, NoSuchGameException
from paper_tactics.ports.logger import Logger
from paper_tactics.ports.player_notifier import PlayerNotifier
from paper_tactics.use_cases.notify_player import (
    notify_active_player,
    notify_passive_player,
)


def concede(
    game_repository: GameRepository,
    player_notifier: PlayerNotifier,
    logger: Logger,
    game_id: Optional[str],
    player_id: str,
) -> None:
    if not game_id:
        return player_notifier.pong(player_id)

    try:
        game = game_repository.fetch(game_id)
    except NoSuchGameException as e:
        return logger.log_exception(e)

    for player in game.active_player, game.passive_player:
        if player.id == player_id:
            player.is_gone = True

    notify_active_player(player_notifier, game, logger)
    notify_passive_player(player_notifier, game, logger)
    game_repository.store(game)
