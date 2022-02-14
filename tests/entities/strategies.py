from hypothesis.strategies import composite, dictionaries, integers, text

from paper_tactics.entities.game import Game
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.entities.player import Player


@composite
def match_requests(draw) -> MatchRequest:
    return MatchRequest(draw(text(min_size=1)), draw(dictionaries(text(), text())))


@composite
def players(draw) -> Player:
    return Player(draw(text(min_size=1)), view_data=draw(dictionaries(text(), text())))


@composite
def games(draw, shallow=False) -> Game:
    size = draw(integers(min_value=2, max_value=7))
    turn_number = draw(integers(min_value=0, max_value=size * size * 2))

    if shallow:
        game = Game(size=size)
    else:
        game = Game(
            id=draw(text(min_size=1)),
            size=size,
            active_player=draw(players()),
            passive_player=draw(players()),
        )

    game.init_players()

    for i in range(turn_number):
        reachable = list(game.active_player.reachable)

        if not reachable:
            break

        turn = reachable[draw(integers(min_value=0, max_value=len(reachable) - 1))]
        game.make_turn(game.active_player.id, turn)

    return game
