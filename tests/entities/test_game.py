from hypothesis import given

from tests.entities.strategies import games


@given(games(shallow=True))
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


@given(games(shallow=True))
def test_units_and_walls_and_reachable_cells_are_valid(game):
    sets = (
        game.active_player.units,
        game.active_player.walls,
        game.active_player.reachable,
        game.passive_player.units,
        game.passive_player.walls,
        game.passive_player.reachable,
    )
    for cells in sets:
        for x, y in cells:
            assert 1 <= x <= game.size and 1 <= y <= game.size


@given(games(shallow=True))
def test_own_walls_and_units_are_not_reachable(game):
    for player in game.active_player, game.passive_player:
        assert player.reachable.isdisjoint(player.units.union(player.walls))


@given(games(shallow=True))
def test_opponents_walls_are_not_reachable(game):
    players = game.active_player, game.passive_player
    for player, opponent in zip(players, reversed(players)):
        assert player.reachable.isdisjoint(opponent.walls)


@given(games(shallow=True))
def test_unit_advantage_is_no_more_than_3(game):
    assert abs(len(game.active_player.units) - len(game.passive_player.units)) <= 3


@given(games(shallow=True))
def test_players_cannot_be_both_defeated(game):
    assert not game.active_player.is_defeated or not game.passive_player.is_defeated


@given(games(shallow=True))
def test_player_cannot_be_defeated_while_having_reachable_cells(game):
    for player in game.active_player, game.passive_player:
        assert not (player.is_defeated and player.reachable)
