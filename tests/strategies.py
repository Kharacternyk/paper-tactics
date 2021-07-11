from hypothesis.strategies import integers
from hypothesis.strategies import lists
from hypothesis.strategies import tuples

import app.game

_integers = integers(min_value=1, max_value=10)
cells = tuples(_integers, _integers)


def _game_with_turns(turns):
    game = app.game.Game()
    for i in turns:
        reachable = list(game.active_player.reachable)
        game.make_turn(*reachable[i % len(reachable)])
    game._turns = turns
    return game


games = lists(integers(min_value=0, max_value=99)).map(_game_with_turns)
