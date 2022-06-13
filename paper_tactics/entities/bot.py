from random import choice

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game_view import GameView


class GameBot:
    def make_turn(self, game_view: GameView) -> Cell:
        return choice(list(game_view.me.reachable))
