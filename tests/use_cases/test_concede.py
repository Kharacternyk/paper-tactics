from hypothesis import given
from hypothesis.strategies import booleans

from paper_tactics.entities.game import Game
from paper_tactics.use_cases.concede import concede
from tests.entities.strategies import games
from tests.use_cases.mocked_ports import (
    MockedGameRepository,
    MockedLogger,
    MockedPlayerNotifier,
)
from tests.use_cases.strategies import player_notifiers


@given(player_notifiers(), games(), booleans())
def test_both_players_are_notified_when_someone_concedes(
    player_notifier: MockedPlayerNotifier, game: Game, is_conceding_player_active: bool
):
    game_repository = MockedGameRepository({game.id: game})
    logger = MockedLogger()

    if is_conceding_player_active:
        conceding_player = game.active_player
        opponent = game.passive_player
    else:
        conceding_player = game.passive_player
        opponent = game.active_player

    concede(game_repository, player_notifier, logger, game.id, conceding_player.id)

    assert (
        conceding_player.id in player_notifier.notified_player_ids
        and opponent.id in player_notifier.notified_player_ids
    )
