from hypothesis.strategies import composite
from hypothesis.strategies import integers

import paper_tactics.game


@composite
def games(draw):
    size = draw(integers(min_value=2, max_value=7))
    game = paper_tactics.game.Game(size)
    turn_number = draw(integers(min_value=0, max_value=size * size * 2))
    for i in range(turn_number):
        reachable = list(game.active_player.reachable)
        if not reachable:
            break
        turn = reachable[draw(integers(min_value=0, max_value=len(reachable) - 1))]
        game.make_turn(*turn)
    return game
