from hypothesis import given
from moto import mock_dynamodb

from paper_tactics.adapters.in_memory_match_request_queue import (
    InMemoryMatchRequestQueue,
)
from tests.adapters.strategies import dynamodb_match_request_queues
from tests.entities.strategies import game_preferences, match_requests


def _test_pop_on_empty_queue_returns_none(queue, preferences):
    assert queue.pop(preferences) is None


def _test_request_is_popped_after_stored_and_read_back(queue, request):
    queue.put(request)

    assert queue.pop(request.game_preferences) == request
    assert queue.pop(request.game_preferences) is None


@mock_dynamodb
@given(dynamodb_match_request_queues(), game_preferences())
def test_pop_on_empty_queue_returns_none_in_dynamodb(queue, preferences):
    _test_pop_on_empty_queue_returns_none(queue, preferences)


@mock_dynamodb
@given(dynamodb_match_request_queues(), match_requests())
def test_request_is_popped_after_stored_and_read_back_in_dynamodb(queue, request):
    _test_request_is_popped_after_stored_and_read_back(queue, request)


@given(game_preferences())
def test_pop_on_empty_queue_returns_none_in_memory(preferences):
    _test_pop_on_empty_queue_returns_none(InMemoryMatchRequestQueue(), preferences)


@given(match_requests())
def test_request_is_popped_after_stored_and_read_back_in_memory(request):
    _test_request_is_popped_after_stored_and_read_back(
        InMemoryMatchRequestQueue(), request
    )
