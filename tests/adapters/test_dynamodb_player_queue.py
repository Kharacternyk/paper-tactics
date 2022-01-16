from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import text
from moto import mock_dynamodb2

from tests.adapters.strategies import dynamodb_player_queues


@mock_dynamodb2
@given(dynamodb_player_queues())
@settings(max_examples=10)
def test_pop_on_empty_player_queue_returns_none(player_queue):
    assert player_queue.pop() is None


@mock_dynamodb2
@given(dynamodb_player_queues(), text(min_size=1))
@settings(max_examples=10)
def test_player_id_is_popped_after_stored_and_read_back(player_queue, player_id):
    player_queue.put(player_id)

    assert player_queue.pop() == player_id
    assert player_queue.pop() is None
