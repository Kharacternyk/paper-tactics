from hypothesis import given
from hypothesis import settings
from moto import mock_dynamodb2

from tests.adapters.strategies import dynamodb_match_request_queues
from tests.entities.strategies import match_requests


@mock_dynamodb2
@given(dynamodb_match_request_queues())
@settings(max_examples=10)
def test_pop_on_empty_queue_returns_none(queue):
    assert queue.pop() is None


@mock_dynamodb2
@given(dynamodb_match_request_queues(), match_requests())
@settings(max_examples=10)
def test_player_id_is_popped_after_stored_and_read_back(queue, request):
    queue.put(request)

    assert queue.pop() == request
    assert queue.pop() is None
