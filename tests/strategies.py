from hypothesis.strategies import composite
from hypothesis.strategies import integers
from hypothesis.strategies import tuples

import paper_tactics.game

_integers = integers(min_value=1, max_value=10)
cells = tuples(_integers, _integers)


@composite
def games(draw):
    game = paper_tactics.game.Game()
    turn_number = draw(integers(min_value=0, max_value=200))
    for i in range(turn_number):
        reachable = list(game.active_player.reachable)
        if not reachable:
            break
        turn = reachable[draw(integers(min_value=0, max_value=len(reachable) - 1))]
        game.make_turn(*turn)
    return game
