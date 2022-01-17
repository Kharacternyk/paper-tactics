from hypothesis import given
from hypothesis.strategies import text

from paper_tactics.use_cases.create_game import create_game
from tests.use_cases.mocked_ports import MockedGameRepository
from tests.use_cases.mocked_ports import MockedLogger
from tests.use_cases.mocked_ports import MockedPlayerNotifier
from tests.use_cases.mocked_ports import MockedPlayerQueue
from tests.use_cases.strategies import player_notifiers
from tests.use_cases.strategies import player_queues


@given(player_queues(), player_notifiers(), text())
def test_game_is_stored_if_and_only_if_no_players_are_gone(
    player_queue: MockedPlayerQueue,
    player_notifier: MockedPlayerNotifier,
    player_id: str,
):
    game_repository = MockedGameRepository()
    logger = MockedLogger()
    opponent_id = player_queue.player_id
    create_game(game_repository, player_queue, player_notifier, logger, player_id)

    if game_repository.stored_games:
        assert (
            not player_notifier.active_player_is_gone
            and not player_notifier.passive_player_is_gone
        )
    elif not opponent_id or opponent_id == player_id:
        assert player_queue.player_id is not None
    else:
        assert (
            player_notifier.active_player_is_gone
            or player_notifier.passive_player_is_gone
        )


@given(player_queues(), player_notifiers(), text())
def test_both_players_are_notified_if_and_only_if_a_game_has_been_stored(
    player_queue: MockedPlayerQueue,
    player_notifier: MockedPlayerNotifier,
    player_id: str,
):
    game_repository = MockedGameRepository()
    logger = MockedLogger()
    opponent_id = player_queue.player_id
    create_game(game_repository, player_queue, player_notifier, logger, player_id)

    if game_repository.stored_games:
        assert (
            player_id in player_notifier.notified_player_ids
            and opponent_id in player_notifier.notified_player_ids
            and len(player_notifier.notified_player_ids) == 2
        )
    else:
        assert len(player_notifier.notified_player_ids) < 2
