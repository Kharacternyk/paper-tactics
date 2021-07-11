from hypothesis import given
from hypothesis import note

import app.game
from .strategies import cells
from .strategies import games


@given(cells)
def test_adjacent_gives_3_or_5_or_8_cells(cell):
    adjacent = app.game.adjacent_cells(*cell)
    assert len(list(adjacent)) in (3, 5, 8)


@given(games())
def test_sets_do_not_overlap(game):
    sets = (
        game.active_player.units,
        game.active_player.walls,
        game.passive_player.units,
        game.passive_player.walls,
    )
    note(str(game))
    for a in sets:
        for b in sets:
            assert a is b or a.isdisjoint(b)
