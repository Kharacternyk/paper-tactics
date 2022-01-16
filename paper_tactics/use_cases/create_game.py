from paper_tactics.entities.game import Game
from paper_tactics.entities.player import Player
from paper_tactics.ports.game_repository import GameRepository
from paper_tactics.ports.player_notifier import PlayerGoneException
from paper_tactics.ports.player_notifier import PlayerNotifier
from paper_tactics.ports.player_queue import PlayerQueue


def create_game(
    game_repository: GameRepository,
    player_queue: PlayerQueue,
    player_notifier: PlayerNotifier,
    player_id: str,
) -> None:
    queued_player_id = player_queue.pop()

    if not queued_player_id or queued_player_id == player_id:
        player_queue.put(player_id)
        return

    active_player = Player(id=queued_player_id)
    passive_player = Player(id=player_id)
    game = Game(active_player=active_player, passive_player=passive_player)

    game.init_players()

    try:
        player_notifier.notify(queued_player_id, game)
    except PlayerGoneException:
        player_queue.put(player_id)
        return

    try:
        player_notifier.notify(player_id, game)
    except PlayerGoneException:
        return

    game_repository.store(game)
