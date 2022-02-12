from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import text
from moto import mock_dynamodb2
from pytest import raises

from paper_tactics.ports.game_repository import NoSuchGameException
from tests.adapters.strategies import dynamodb_game_repositories
from tests.entities.strategies import games


@mock_dynamodb2
@given(dynamodb_game_repositories(), games())
@settings(max_examples=5)
def test_game_is_not_changed_if_written_and_read_back(game_repository, game):
    game_repository.store(game)

    assert game_repository.fetch(game.id) == game


@mock_dynamodb2
@given(dynamodb_game_repositories(), text())
@settings(max_examples=10)
def test_no_such_game_exception_is_thrown_if_game_does_not_exist(
    game_repository, game_id
):
    with raises(NoSuchGameException):
        game_repository.fetch(game_id)
