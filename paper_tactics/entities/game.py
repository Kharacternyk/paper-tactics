from dataclasses import dataclass, field
from typing import Final, Iterable, cast

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game_bot import GameBot
from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.game_view import GameView
from paper_tactics.entities.player import Player
from paper_tactics.entities.player_view import PlayerView


@dataclass
class Game:
    id: Final[str] = ""
    preferences: Final[GamePreferences] = field(default_factory=GamePreferences)
    turns_left: int = 0
    active_player: Player = field(default_factory=Player)
    passive_player: Player = field(default_factory=Player)

    def init_players(self) -> None:
        assert self.active_player.id != self.passive_player.id
        self.active_player.units.add((1, 1))
        self.passive_player.units.add((self.preferences.size, self.preferences.size))
        self._rebuild_reachable_set(self.active_player, self.passive_player)
        self._rebuild_reachable_set(self.passive_player, self.active_player)
        self.turns_left = self.preferences.turn_count

    def get_view(self, player_id: str) -> GameView:
        if player_id == self.active_player.id:
            me = self.active_player
            opponent = self.passive_player
        elif player_id == self.passive_player.id:
            me = self.passive_player
            opponent = self.active_player
        else:
            raise ValueError("No such player")

        if self.preferences.is_visibility_applied and me.can_win and opponent.can_win:
            opponent_units = opponent.units.intersection(me.visible)
        else:
            opponent_units = opponent.units

        return GameView(
            id=self.id,
            turns_left=self.turns_left,
            my_turn=(me == self.active_player),
            me=PlayerView(
                units=cast(frozenset[Cell], me.units),
                walls=cast(frozenset[Cell], me.walls),
                reachable=cast(frozenset[Cell], me.reachable),
                view_data=me.view_data.copy(),
                is_gone=me.is_gone,
                is_defeated=me.is_defeated,
            ),
            opponent=PlayerView(
                units=cast(frozenset[Cell], opponent_units),
                walls=cast(frozenset[Cell], opponent.walls),
                reachable=frozenset(),
                view_data=opponent.view_data.copy(),
                is_gone=opponent.is_gone,
                is_defeated=opponent.is_defeated,
            ),
        )

    def make_turn(self, player_id: str, cell: Cell) -> None:
        if (
            player_id != self.active_player.id
            or cell not in self.active_player.reachable
            or not all(
                player.can_win for player in (self.active_player, self.passive_player)
            )
        ):
            raise IllegalTurnException(self.id, player_id, cell)

        self._make_turn(cell, self.active_player, self.passive_player)
        self._decrement_turns()

    def get_adjacent_cells(self, cell: Cell) -> Iterable[Cell]:
        x, y = cell
        for x_ in (x - 1, x, x + 1):
            for y_ in (y - 1, y, y + 1):
                if self.is_valid_cell((x_, y_)) and (x_ != x or y_ != y):
                    yield x_, y_

    def is_valid_cell(self, cell: Cell) -> bool:
        x, y = cell
        return 1 <= x <= self.preferences.size and 1 <= y <= self.preferences.size

    def _decrement_turns(self) -> None:
        self.turns_left -= 1
        if not self.turns_left:
            if self.preferences.is_against_bot:
                game_bot = GameBot()
                for i in range(self.preferences.turn_count):
                    if not self.passive_player.reachable:
                        self.passive_player.is_defeated = True
                        break
                    cell = game_bot.make_turn(self.get_view(self.passive_player.id))
                    assert cell in self.passive_player.reachable
                    self._make_turn(cell, self.passive_player, self.active_player)
            else:
                self.active_player, self.passive_player = (
                    self.passive_player,
                    self.active_player,
                )
            self.turns_left = self.preferences.turn_count
        if not self.active_player.reachable and not self.passive_player.is_defeated:
            self.active_player.is_defeated = True

    def _make_turn(self, cell: Cell, player: Player, opponent: Player) -> None:
        if cell in opponent.units:
            opponent.units.remove(cell)
            player.walls.add(cell)
            self._rebuild_reachable_set(opponent, player)
        else:
            player.units.add(cell)

        if self._is_opening:
            player.reachable.remove(cell)
            for adjacent_cell in self.get_adjacent_cells(cell):
                if adjacent_cell not in player.units:
                    player.reachable.add(adjacent_cell)
                    if self.preferences.is_visibility_applied:
                        player.visible.add(adjacent_cell)
        else:
            self._rebuild_reachable_set(player, opponent)

    @property
    def _is_opening(self) -> bool:
        return not self.active_player.walls and not self.passive_player.walls

    def _rebuild_reachable_set(self, player: Player, opponent: Player) -> None:
        player.reachable.clear()
        if self.preferences.is_visibility_applied:
            player.visible = {cell for cell in player.visible if cell in opponent.units}
        sources = player.units.copy()
        while True:
            new_sources = set()
            for source in sources:
                for cell in self.get_adjacent_cells(source):
                    if self.preferences.is_visibility_applied:
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


class IllegalTurnException(Exception):
    pass
