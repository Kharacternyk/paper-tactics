from hypothesis import assume, given
from hypothesis.strategies import data, sampled_from

from paper_tactics.entities.game import Game
from paper_tactics.use_cases.make_turn import make_turn
from tests.entities.strategies import games
from tests.use_cases.mocked_ports import (
    MockedGameRepository,
    MockedLogger,
    MockedPlayerNotifier,
)
from tests.use_cases.strategies import player_notifiers


@given(player_notifiers(), games(), data())
def test_game_is_updated_if_the_turn_is_legal(
    player_notifier: MockedPlayerNotifier, game: Game, data
):
    game_repository = MockedGameRepository({game.id: game})
    logger = MockedLogger()
    assume(game.active_player.reachable)
    cell = data.draw(sampled_from(list(game.active_player.reachable)))

    make_turn(
        game_repository, player_notifier, logger, game.id, game.active_player.id, cell
    )

    assert game_repository.stored_games[game.id] is not game
