from fakeredis import FakeRedis
from hypothesis import given
from hypothesis.strategies import text

from paper_tactics.adapters.redis_match_request_queue import RedisMatchRequestQueue
from tests.entities.strategies import match_requests


@given(text(min_size=1))
def test_pop_on_empty_queue_returns_none(key):
    queue = RedisMatchRequestQueue(FakeRedis(decode_responses=True), key)
    assert queue.pop() is None


@given(text(min_size=1), match_requests())
def test_request_is_popped_after_stored_and_read_back(key, request):
    queue = RedisMatchRequestQueue(FakeRedis(decode_responses=True), key)
    queue.put(request)

    assert queue.pop() == request
    assert queue.pop() is None
