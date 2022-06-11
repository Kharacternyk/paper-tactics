from dataclasses import dataclass, field
from typing import Iterable

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game_view import GameView
from paper_tactics.entities.player import Player
from paper_tactics.entities.player_view import PlayerView


@dataclass
class Game:
    id: str = ""
    size: int = 10
    turns_left: int = 3
    active_player: Player = field(default_factory=Player)
    passive_player: Player = field(default_factory=Player)

    def init_players(self) -> None:
        self.active_player.units.add((1, 1))
        self.passive_player.units.add((self.size, self.size))
        self._rebuild_reachable_set(self.active_player, self.passive_player)
        self._rebuild_reachable_set(self.passive_player, self.active_player)

    def get_view(self, player_id: str) -> GameView:
        if player_id == self.active_player.id:
            me = self.active_player
            opponent = self.passive_player
        elif player_id == self.passive_player.id:
            me = self.passive_player
            opponent = self.active_player
        else:
            raise ValueError("No such player")

        if me.can_win and opponent.can_win:
            opponent_units = opponent.units.intersection(me.visible)
        else:
            opponent_units = opponent.units.copy()

        return GameView(
            id=self.id,
            size=self.size,
            turns_left=self.turns_left,
            my_turn=(me == self.active_player),
            me=PlayerView(
                units=me.units.copy(),
                walls=me.walls.copy(),
                reachable=me.reachable.copy(),
                view_data=me.view_data.copy(),
                is_gone=me.is_gone,
                is_defeated=me.is_defeated,
            ),
            opponent=PlayerView(
                units=opponent_units,
                walls=opponent.walls.copy(),
                reachable=set(),
                view_data=opponent.view_data.copy(),
                is_gone=opponent.is_gone,
                is_defeated=opponent.is_defeated,
            ),
        )

    def make_turn(self, player_id: str, cell: Cell) -> None:
        if (
            player_id != self.active_player.id
            or cell not in self.active_player.reachable
        ):
            raise IllegalTurnException(self.id, player_id, cell)

        if cell in self.passive_player.units:
            self.passive_player.units.remove(cell)
            self.active_player.walls.add(cell)
            self._rebuild_reachable_set(self.passive_player, self.active_player)
        else:
            self.active_player.units.add(cell)

        self._rebuild_reachable_set(self.active_player, self.passive_player)
        self._decrement_turns()

    def get_adjacent_cells(self, cell: Cell) -> Iterable[Cell]:
        x, y = cell
        for x_ in (x - 1, x, x + 1):
            for y_ in (y - 1, y, y + 1):
                if self.is_valid_cell((x_, y_)) and (x_ != x or y_ != y):
                    yield x_, y_

    def is_valid_cell(self, cell: Cell) -> bool:
        x, y = cell
        return 1 <= x <= self.size and 1 <= y <= self.size

    def _rebuild_reachable_set(self, player: Player, opponent: Player) -> None:
        player.reachable.clear()
        player.visible = {cell for cell in player.visible if cell in opponent.units}
        sources = player.units.copy()
        while True:
            new_sources = set()
            for source in sources:
                for cell in self.get_adjacent_cells(source):
                    player.visible.add(cell)
                    if cell in sources:
                        continue
                    if cell in player.walls:
                        new_sources.add(cell)
                    elif cell not in opponent.walls and cell not in player.units:
                        player.reachable.add(cell)
            if not new_sources:
                break
            sources.update(new_sources)

    def _decrement_turns(self) -> None:
        self.turns_left -= 1
        if not self.turns_left:
            self.active_player, self.passive_player = (
                self.passive_player,
                self.active_player,
            )
            self.turns_left = 3
        if not self.active_player.reachable:
            self.active_player.is_defeated = True


class IllegalTurnException(Exception):
    pass
