from hypothesis import given, settings

from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.use_cases.create_game import create_game
from tests.entities.strategies import match_requests
from tests.use_cases.mocked_ports import (
    MockedGameRepository,
    MockedLogger,
    MockedMatchRequestQueue,
    MockedPlayerNotifier,
)
from tests.use_cases.strategies import match_request_queues, player_notifiers


@given(match_request_queues(), player_notifiers(), match_requests())
def test_game_is_stored_only_if_no_players_are_gone(
    match_request_queue: MockedMatchRequestQueue,
    player_notifier: MockedPlayerNotifier,
    request: MatchRequest,
):
    game_repository = MockedGameRepository()
    logger = MockedLogger()
    create_game(game_repository, match_request_queue, player_notifier, logger, request)

    if game_repository.stored_games:
        assert (
            not player_notifier.active_player_is_gone
            and not player_notifier.passive_player_is_gone
        )


@given(match_request_queues(), player_notifiers(), match_requests())
@settings(max_examples=4)
def test_players_are_notified_if_a_game_is_created(
    match_request_queue: MockedMatchRequestQueue,
    player_notifier: MockedPlayerNotifier,
    request: MatchRequest,
):
    game_repository = MockedGameRepository()
    logger = MockedLogger()
    create_game(game_repository, match_request_queue, player_notifier, logger, request)

    if game_repository.stored_games:
        assert request.id in player_notifier.notified_player_ids
