from hypothesis.strategies import composite
from hypothesis.strategies import integers

from paper_tactics.game import Game


@composite
def games(draw):
    size = draw(integers(min_value=2, max_value=7))
    turn_number = draw(integers(min_value=0, max_value=size * size * 2))

    game = Game(size=size)
    game.init_players()

    for i in range(turn_number):
        reachable = list(game.active_player.reachable)

        if not reachable:
            break

        turn = reachable[draw(integers(min_value=0, max_value=len(reachable) - 1))]
        game.make_turn(*turn)

    return game
