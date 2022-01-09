from hypothesis import given

from .strategies import games
from paper_tactics.game_io import deserialize_from_dynamodb_dict
from paper_tactics.game_io import serialize_to_dynamodb_dict


@given(games())
def test_deserialize_is_inverse_of_serialize(game):
    assert game == deserialize_from_dynamodb_dict(serialize_to_dynamodb_dict(game))
