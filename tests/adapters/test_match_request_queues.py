from hypothesis import given, settings
from moto import mock_dynamodb2

from paper_tactics.adapters.in_memory_match_request_queue import (
    InMemoryMatchRequestQueue,
)
from tests.adapters.strategies import (
    dynamodb_match_request_queues,
    redis_match_request_queues,
)
from tests.entities.strategies import match_requests


def _test_pop_on_empty_queue_returns_none(queue):
    assert queue.pop() is None


def _test_request_is_popped_after_stored_and_read_back(queue, request):
    queue.put(request)

    assert queue.pop() == request
    assert queue.pop() is None


@mock_dynamodb2
@given(dynamodb_match_request_queues())
@settings(max_examples=10)
def test_pop_on_empty_queue_returns_none_in_dynamodb(queue):
    _test_pop_on_empty_queue_returns_none(queue)


@mock_dynamodb2
@given(dynamodb_match_request_queues(), match_requests())
@settings(max_examples=10)
def test_request_is_popped_after_stored_and_read_back_in_dynamodb(queue, request):
    _test_request_is_popped_after_stored_and_read_back(queue, request)


@given(redis_match_request_queues())
def test_pop_on_empty_queue_returns_none_in_redis(queue):
    _test_pop_on_empty_queue_returns_none(queue)


@given(redis_match_request_queues(), match_requests())
def test_request_is_popped_after_stored_and_read_back(queue, request):
    _test_request_is_popped_after_stored_and_read_back(queue, request)


def test_pop_on_empty_queue_returns_none_in_memory():
    _test_pop_on_empty_queue_returns_none(InMemoryMatchRequestQueue())


@given(match_requests())
def test_request_is_popped_after_stored_and_read_back_in_memory(request):
    _test_request_is_popped_after_stored_and_read_back(
        InMemoryMatchRequestQueue(), request
    )
