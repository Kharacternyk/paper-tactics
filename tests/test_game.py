from hypothesis import given

import app.game
from .strategies import cells
from .strategies import games


@given(cells)
def test_adjacent_gives_3_or_5_or_8_cells(cell):
    adjacent = app.game.adjacent_cells(*cell)
    assert len(list(adjacent)) in (3, 5, 8)


@given(games)
def test_unit_and_wall_count(game):
    total_units = len(game.active_player.units) + len(game.passive_player.units)
    total_walls = len(game.active_player.walls) + len(game.passive_player.walls)
    assert len(game._turns) == (total_units - 2) + 2 * total_walls


@given(games)
def test_sets_do_not_overlap(game):
    sets = (
        game.active_player.units,
        game.active_player.walls,
        game.passive_player.units,
        game.passive_player.walls,
    )
    for a in sets:
        for b in sets:
            assert a is b or a.isdisjoint(b)
