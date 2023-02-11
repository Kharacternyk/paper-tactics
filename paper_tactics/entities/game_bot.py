from dataclasses import dataclass
from random import choices

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game_view import GameView


@dataclass(frozen=True)
class GameBot:
    opponent_unit_weight: float = 7
    trench_weight: float = 5

    def make_turn(self, game_view: GameView) -> Cell:
        weights = [self._get_weight(cell, game_view) for cell in game_view.me.reachable]
        return choices(list(game_view.me.reachable), weights)[0]

    def _get_weight(self, cell: Cell, game_view: GameView) -> float:
        if cell in game_view.trenches:
            return self.trench_weight
        if cell in game_view.opponent.units:
            return self.opponent_unit_weight
        return 1
