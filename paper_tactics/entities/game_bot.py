from dataclasses import dataclass
from random import choices

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game_view import GameView


@dataclass
class GameBot:
    opponent_unit_weight: int = 7

    def make_turn(self, game_view: GameView) -> Cell:
        weights = [
            1 if cell not in game_view.opponent.units else self.opponent_unit_weight
            for cell in game_view.me.reachable
        ]
        return choices(list(game_view.me.reachable), weights)[0]
