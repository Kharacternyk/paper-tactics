from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game import IllegalTurnException
from paper_tactics.ports.game_repository import GameRepository
from paper_tactics.ports.game_repository import NoSuchGameException
from paper_tactics.ports.player_notifier import PlayerGoneException
from paper_tactics.ports.player_notifier import PlayerNotifier


def make_turn(
    game_repository: GameRepository,
    player_notifier: PlayerNotifier,
    game_id: str,
    player_id: str,
    cell: Cell,
) -> None:
    try:
        game = game_repository.fetch(game_id)
    except NoSuchGameException:
        return

    if game.active_player.id != player_id:
        return

    try:
        game.make_turn(cell)
    except IllegalTurnException:
        return

    try:
        player_notifier.notify(game.active_player.id, game)
    except PlayerGoneException:
        game.active_player.reachable = set()
        game_repository.store(game)
        try:
            player_notifier.notify(game.passive_player.id, game)
        except PlayerGoneException:
            pass
        return

    try:
        player_notifier.notify(game.passive_player.id, game)
    except PlayerGoneException:
        game.passive_player.reachable = set()
        game_repository.store(game)
        try:
            player_notifier.notify(game.active_player.id, game)
        except PlayerGoneException:
            pass
        return

    game_repository.store(game)
