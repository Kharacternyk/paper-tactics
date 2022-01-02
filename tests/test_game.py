from hypothesis import given

from .strategies import games


@given(games())
def test_units_and_walls_do_not_overlap(game):
    sets = (
        game.active_player.units,
        game.active_player.walls,
        game.passive_player.units,
        game.passive_player.walls,
    )
    for a in sets:
        for b in sets:
            assert a is b or a.isdisjoint(b)


@given(games())
def test_own_walls_and_units_are_not_reachable(game):
    for player in game.active_player, game.passive_player:
        assert player.reachable.isdisjoint(player.units.union(player.walls))


@given(games())
def test_opponents_walls_are_not_reachable(game):
    players = game.active_player, game.passive_player
    for player, opponent in zip(players, reversed(players)):
        assert player.reachable.isdisjoint(opponent.walls)


@given(games())
def test_unit_advantage_is_no_more_than_3(game):
    assert abs(len(game.active_player.units) - len(game.passive_player.units)) <= 3
