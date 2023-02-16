from paper_tactics.entities.game import Game
from paper_tactics.ports.logger import Logger
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


def notify_active_player(
    player_notifier: PlayerNotifier,
    game: Game,
    logger: Logger,
) -> bool:
    try:
        player_notifier.notify(
            game.active_player.id, game.get_view(game.active_player.id)
        )
    except PlayerGoneException as e:
        game.active_player.is_gone = True
        logger.log_exception(e)
        return False
    return True


def notify_passive_player(
    player_notifier: PlayerNotifier,
    game: Game,
    logger: Logger,
) -> bool:
    if not game.preferences.is_against_bot:
        try:
            player_notifier.notify(
                game.passive_player.id, game.get_view(game.passive_player.id)
            )
        except PlayerGoneException as e:
            game.passive_player.is_gone = True
            logger.log_exception(e)
            return False
    return True
