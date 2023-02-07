from hypothesis import given
from hypothesis.strategies import text
from moto import mock_dynamodb
from pytest import raises

from paper_tactics.adapters.in_memory_game_repository import InMemoryGameRepository
from paper_tactics.ports.game_repository import NoSuchGameException
from tests.adapters.strategies import dynamodb_game_repositories
from tests.entities.strategies import games


def _test_game_is_not_changed_if_written_and_read_back(game_repository, game):
    game_repository.store(game)

    assert game_repository.fetch(game.id) == game


def _test_no_such_game_exception_is_thrown_if_game_does_not_exist(
    game_repository, game_id
):
    with raises(NoSuchGameException):
        game_repository.fetch(game_id)


@mock_dynamodb
@given(dynamodb_game_repositories(), games())
def test_game_is_not_changed_if_written_and_read_back_in_dynamodb(
    game_repository, game
):
    _test_game_is_not_changed_if_written_and_read_back(game_repository, game)


@mock_dynamodb
@given(dynamodb_game_repositories(), text(min_size=1))
def test_no_such_game_exception_is_thrown_if_game_does_not_exist_in_dynamodb(
    game_repository, game_id
):
    _test_no_such_game_exception_is_thrown_if_game_does_not_exist(
        game_repository, game_id
    )


@given(games())
def test_game_is_not_changed_if_written_and_read_back_in_memory(game):
    _test_game_is_not_changed_if_written_and_read_back(InMemoryGameRepository(), game)


@given(text())
def test_no_such_game_exception_is_thrown_if_game_does_not_exist_in_memory(game_id):
    _test_no_such_game_exception_is_thrown_if_game_does_not_exist(
        InMemoryGameRepository(), game_id
    )
