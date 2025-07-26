from dataclasses import dataclass
from random import choice, randint

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game_view import GameView


@dataclass(frozen=True)
class GameBot:
    def most_discovered_territory(self, game_view: GameView) -> Cell:
        sorted_by_reachability = []
        for cell in game_view.me.reachable:
            discovered_cells_for_this_cell = 0
            for x, y in game_view.preferences.get_adjacent_cells(cell):
                if (x, y) not in game_view.me.reachable:
                    discovered_cells_for_this_cell += 1
            sorted_by_reachability.append((discovered_cells_for_this_cell, cell))
        sorted_by_reachability.sort()
        sorted_by_reachability.reverse()
        return sorted_by_reachability
    
    def can_clear_opponent(self, game_view: GameView, cell: Cell, turns_left: int) -> int:
        amount_of_opponent_units = 0
        for x, y in game_view.preferences.get_adjacent_cells(cell):
            if (x, y) in game_view.opponent.units:
                amount_of_opponent_units += 1
        if turns_left > amount_of_opponent_units:
            return True
        return False
        
    def opponent_walls_near_cell(self, game_view: GameView, cell: Cell) -> bool:
        amount_of_opponent_walls = 0
        for x, y in game_view.preferences.get_adjacent_cells(cell):
            if (x, y) in game_view.opponent.walls:
                amount_of_opponent_walls += 1
        return amount_of_opponent_walls
    
    def reachable_opponent_units(self, game_view: GameView) -> list:
        return list(game_view.me.reachable & game_view.opponent.units)
    
    def adjacent_opponent_units(self, game_view: GameView) -> list:
        adjacent_opponent_units_list = []
        for cell in game_view.opponent.units:
            if any(cell_ in game_view.me.units for cell_ in game_view.preferences.get_adjacent_cells(cell)):
                adjacent_opponent_units_list.append(cell)
        return adjacent_opponent_units_list

    def make_turn(self, game_view: GameView, turns_left) -> Cell:
        aou = self.adjacent_opponent_units(game_view)
        rou = self.reachable_opponent_units(game_view)
        mdt = self.most_discovered_territory(game_view)
        safe_cells = list(game_view.me.reachable - game_view.opponent.reachable)
        if len(game_view.me.units) + len(game_view.opponent.walls) == 1:
            return mdt[-1][1]
        if aou and randint(1, 20) < 20:
            return choice(aou)
        if rou and randint(1, 5) < 5:
            return choice(rou)
        for _, cell in mdt:
            if self.can_clear_opponent(game_view, cell, turns_left) and self.opponent_walls_near_cell(game_view, cell) < randint(0, 4):
                return cell
        if safe_cells:
            return choice(safe_cells)
        return choice(list(game_view.me.reachable))


