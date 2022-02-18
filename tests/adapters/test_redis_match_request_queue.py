from hypothesis import given

from tests.adapters.strategies import redis_match_request_queues
from tests.entities.strategies import match_requests


@given(redis_match_request_queues())
def test_pop_on_empty_queue_returns_none(queue):
    assert queue.pop() is None


@given(redis_match_request_queues(), match_requests())
def test_request_is_popped_after_stored_and_read_back(queue, request):
    queue.put(request)

    assert queue.pop() == request
    assert queue.pop() is None
