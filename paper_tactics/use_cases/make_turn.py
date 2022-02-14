from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game import IllegalTurnException
from paper_tactics.ports.game_repository import GameRepository, NoSuchGameException
from paper_tactics.ports.logger import Logger
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


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

    try:
        player_notifier.notify(game.active_player.id, game)
    except PlayerGoneException as e:
        game.active_player.is_gone = True
        game_repository.store(game)
        try:
            player_notifier.notify(game.passive_player.id, game)
        except PlayerGoneException:
            pass
        return logger.log_exception(e)

    try:
        player_notifier.notify(game.passive_player.id, game)
    except PlayerGoneException as e:
        game.passive_player.is_gone = True
        game_repository.store(game)
        try:
            player_notifier.notify(game.active_player.id, game)
        except PlayerGoneException:
            pass
        return logger.log_exception(e)

    game_repository.store(game)
