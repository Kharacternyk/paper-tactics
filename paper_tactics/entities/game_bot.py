from dataclasses import dataclass
from random import choice

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game_view import GameView


@dataclass(frozen=True)
class GameBot:
    def most_discovered_territory(self, game_view: GameView) -> Cell:
        max_discovered_cells = 0
        best_cell = 0
        for cell in game_view.me.reachable:
            discovered_cells_for_this_cell = 0
            for x, y in game_view.preferences.get_adjacent_cells(cell):
                if (x, y) not in game_view.me.reachable:
                    discovered_cells_for_this_cell += 1
            if discovered_cells_for_this_cell > max_discovered_cells:
                max_discovered_cells = discovered_cells_for_this_cell
                best_cell = cell
        return [best_cell, max_discovered_cells]
    
    def can_clear_opponent(self, game_view: GameView, cell: Cell, turns_left: int) -> bool:
        amount_of_opponent_units = 0
        for x, y in game_view.preferences.get_adjacent_cells(cell):
            if (x, y) in game_view.opponent.units:
                amount_of_opponent_units += 1
        if turns_left > amount_of_opponent_units:
            return True
        return False
        
    def opponent_walls_near_cell(self, game_view: GameView, cell: Cell) -> bool:
        for x, y in game_view.preferences.get_adjacent_cells(cell):
            if (x, y) in game_view.opponent.walls:
                return True
        return False
    
    def reachable_opponent_units(self, game_view: GameView) -> list:
        return list(game_view.me.reachable & game_view.opponent.units)
    
    def adjacent_opponent_units(self, game_view: GameView) -> list:
        adjacent_opponent_units_list = []
        for cell in game_view.opponent.units:
            if any(cell_ in game_view.me.units for cell_ in game_view.preferences.get_adjacent_cells(cell)):
                adjacent_opponent_units_list.append(cell)
        return adjacent_opponent_units_list

    def make_turn(self, game_view: GameView, bot_turns_left) -> Cell:
        aou = self.adjacent_opponent_units(game_view)
        rou = self.reachable_opponent_units(game_view)
        mdt = self.most_discovered_territory(game_view)
        ownc = self.opponent_walls_near_cell(game_view, mdt)
        cco = self.can_clear_opponent(game_view, mdt, bot_turns_left)
        safe_cells = list(game_view.me.reachable - game_view.opponent.reachable)
        if aou:
            return choice(aou)
        if rou:
            return choice(rou)
        if cco and not ownc:
            return mdt
        if safe_cells:
            return choice(safe_cells)
        return choice(game_view.me.reachable)


