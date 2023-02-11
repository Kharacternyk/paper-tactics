from dataclasses import dataclass
from random import choices

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game_view import GameView


@dataclass(frozen=True)
class GameBot:
    # TODO not aggressive
    neighbour_opponent_unit_weight: float = 10
    opponent_unit_weight: float = 7
    trench_weight: float = 5
    opponent_wall_weight: float = 0.3
    trap_weight: float = 0.05
    taunt_weight: float = 2
    diagonal_weight: float = 1.5
    horizontal_weight: float = 1
    discoverable_weight: float = 1

    def make_turn(self, game_view: GameView) -> Cell:
        weights = [self._get_weight(cell, game_view) for cell in game_view.me.reachable]
        return choices(list(game_view.me.reachable), weights)[0]

    def _get_weight(self, cell: Cell, game_view: GameView) -> float:
        if cell in game_view.opponent.units:
            if any(
                cell_ in game_view.me.units
                for cell_ in game_view.preferences.get_adjacent_cells(cell)
            ):
                return self.neighbour_opponent_unit_weight
            return self.opponent_unit_weight

        if cell in game_view.trenches:
            return self.trench_weight

        if any(
            cell_ in game_view.opponent.walls
            for cell_ in game_view.preferences.get_adjacent_cells(cell)
        ):
            return self.opponent_wall_weight

        opponent_count = sum(
            1
            for cell_ in game_view.preferences.get_adjacent_cells(cell)
            if cell_ in game_view.opponent.units
        )
        if opponent_count >= game_view.turns_left:
            return self.trap_weight
        if opponent_count > 0:
            return self.taunt_weight

        if not game_view.preferences.is_visibility_applied:
            x, y = cell
            for cell_ in ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)):
                if cell_ in game_view.me.walls or cell_ in game_view.me.units:
                    return self.horizontal_weight
            return self.diagonal_weight

        discoverable_count = sum(
            1
            for cell_ in game_view.preferences.get_adjacent_cells(cell)
            if cell_ not in game_view.me.reachable
        )
        return (discoverable_count + 1) * self.discoverable_weight
