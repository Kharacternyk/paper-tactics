from hypothesis import given

from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.use_cases.create_game import create_game
from tests.entities.strategies import match_requests
from tests.use_cases.mocked_ports import MockedGameRepository
from tests.use_cases.mocked_ports import MockedLogger
from tests.use_cases.mocked_ports import MockedMatchRequestQueue
from tests.use_cases.mocked_ports import MockedPlayerNotifier
from tests.use_cases.strategies import match_request_queues
from tests.use_cases.strategies import player_notifiers


@given(match_request_queues(), player_notifiers(), match_requests())
def test_game_is_stored_if_and_only_if_no_players_are_gone(
    match_request_queue: MockedMatchRequestQueue,
    player_notifier: MockedPlayerNotifier,
    request: MatchRequest,
):
    game_repository = MockedGameRepository()
    logger = MockedLogger()
    queued_request = match_request_queue.request
    create_game(game_repository, match_request_queue, player_notifier, logger, request)

    if game_repository.stored_games:
        assert (
            not player_notifier.active_player_is_gone
            and not player_notifier.passive_player_is_gone
        )
    elif not queued_request or queued_request.id == request.id:
        assert match_request_queue.request is not None
    else:
        assert (
            player_notifier.active_player_is_gone
            or player_notifier.passive_player_is_gone
        )


@given(match_request_queues(), player_notifiers(), match_requests())
def test_both_players_are_notified_if_and_only_if_a_game_has_been_stored(
    match_request_queue: MockedMatchRequestQueue,
    player_notifier: MockedPlayerNotifier,
    request: MatchRequest,
):
    game_repository = MockedGameRepository()
    logger = MockedLogger()
    queued_request = match_request_queue.request
    create_game(game_repository, match_request_queue, player_notifier, logger, request)

    if game_repository.stored_games:
        assert (
            request.id in player_notifier.notified_player_ids
            and queued_request
            and queued_request.id in player_notifier.notified_player_ids
            and len(player_notifier.notified_player_ids) == 2
        )
    else:
        assert len(player_notifier.notified_player_ids) < 2
