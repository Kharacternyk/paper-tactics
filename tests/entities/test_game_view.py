import json

from hypothesis import given

from tests.entities.strategies import games


@given(games())
def test_game_views_are_json_serializable(game):
    for player_id in game.active_player.id, game.passive_player.id:
        json.loads(game.get_view(player_id).to_json())
