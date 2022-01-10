from time import time

from hypothesis import given

from paper_tactics.game.serialization.dynamodb import deserialize
from paper_tactics.game.serialization.dynamodb import serialize
from tests.strategies import games


@given(games())
def test_deserialize_is_inverse_of_serialize(game):
    assert game == deserialize(serialize(game))


@given(games())
def test_serialized_game_contains_valid_expiration_time(game):
    now = time()
    expiration_time = serialize(game)["expiration-time"]

    assert isinstance(expiration_time, int) and expiration_time >= now
