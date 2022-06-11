from hypothesis import assume, given
from hypothesis.strategies import data, integers, sampled_from, text, tuples

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


@given(player_notifiers(), games(), data())
def test_game_is_unmodified_if_the_turn_is_illegal(
    player_notifier: MockedPlayerNotifier, game: Game, data
):
    game_repository = MockedGameRepository({game.id: game})
    logger = MockedLogger()
    coordinates = integers(min_value=1, max_value=game.preferences.size)
    cell = data.draw(tuples(coordinates, coordinates))
    assume(cell not in game.active_player.reachable)

    make_turn(
        game_repository, player_notifier, logger, game.id, game.active_player.id, cell
    )

    assert game_repository.stored_games[game.id] == game


@given(player_notifiers(), games(), data())
def test_game_is_unmodified_if_passive_player_attempts_to_make_a_turn(
    player_notifier: MockedPlayerNotifier, game: Game, data
):
    game_repository = MockedGameRepository({game.id: game})
    logger = MockedLogger()
    coordinates = integers(min_value=1, max_value=game.preferences.size)
    cell = data.draw(tuples(coordinates, coordinates))

    make_turn(
        game_repository, player_notifier, logger, game.id, game.passive_player.id, cell
    )

    assert game_repository.stored_games[game.id] == game


@given(player_notifiers(), games(), data())
def test_player_are_notified_when_a_valid_turn_is_made(
    player_notifier: MockedPlayerNotifier, game: Game, data
):
    game_repository = MockedGameRepository({game.id: game})
    logger = MockedLogger()
    assume(game.active_player.reachable)
    cell = data.draw(sampled_from(list(game.active_player.reachable)))

    make_turn(
        game_repository, player_notifier, logger, game.id, game.active_player.id, cell
    )

    assert (
        game.active_player.id in player_notifier.notified_player_ids
        and game.passive_player.id in player_notifier.notified_player_ids
    )


@given(player_notifiers(), text(), text(), data())
def test_making_turn_in_unexistent_game_is_logged(
    player_notifier: MockedPlayerNotifier, game_id: str, player_id: str, data
):
    game_repository = MockedGameRepository({})
    logger = MockedLogger()
    cell = data.draw(tuples(integers(), integers()))

    make_turn(game_repository, player_notifier, logger, game_id, player_id, cell)

    assert logger.log
