from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game import IllegalTurnException
from paper_tactics.ports.game_repository import GameRepository, NoSuchGameException
from paper_tactics.ports.logger import Logger
from paper_tactics.ports.player_notifier import PlayerNotifier
from paper_tactics.use_cases.notify_player import (
    notify_active_player,
    notify_passive_player,
)


def make_turn(
    game_repository: GameRepository,
    player_notifier: PlayerNotifier,
    logger: Logger,
    game_id: str,
    player_id: str,
    cell: Cell,
) -> None:
    try:
        game = game_repository.fetch(game_id)
    except NoSuchGameException as e:
        return logger.log_exception(e)

    try:
        game.make_turn(player_id, cell)
    except IllegalTurnException as e:
        return logger.log_exception(e)

    if notify_active_player(player_notifier, game, logger):
        if not notify_passive_player(player_notifier, game, logger):
            notify_active_player(player_notifier, game, logger)
    else:
        notify_passive_player(player_notifier, game, logger)

    game_repository.store(game)
