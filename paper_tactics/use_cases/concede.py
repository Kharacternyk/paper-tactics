from paper_tactics.ports.game_repository import GameRepository, NoSuchGameException
from paper_tactics.ports.logger import Logger
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


def concede(
    game_repository: GameRepository,
    player_notifier: PlayerNotifier,
    logger: Logger,
    game_id: str,
    player_id: str,
) -> None:
    try:
        game = game_repository.fetch(game_id)
    except NoSuchGameException as e:
        return logger.log_exception(e)

    for player in game.active_player, game.passive_player:
        if player.id == player_id:
            player.is_gone = True

    for player in game.active_player, game.passive_player:
        try:
            player_notifier.notify(player.id, game)
        except PlayerGoneException:
            pass

    game_repository.store(game)
