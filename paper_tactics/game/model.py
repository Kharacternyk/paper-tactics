from dataclasses import dataclass
from dataclasses import field
from uuid import uuid4

Cell = tuple[int, int]
uuidHex = lambda: uuid4().hex


@dataclass
class Player:
    id: str = field(default_factory=uuidHex)
    units: set[Cell] = field(default_factory=set)
    walls: set[Cell] = field(default_factory=set)
    reachable: set[Cell] = field(default_factory=set)


@dataclass
class Game:
    id: str = field(default_factory=uuidHex)
    size: int = 10
    turns_left: int = 3
    active_player: Player = field(default_factory=Player)
    passive_player: Player = field(default_factory=Player)

    def init_players(self):
        self.active_player.units.add((1, 1))
        self.active_player.reachable.update(self.get_adjacent_cells(1, 1))
        self.passive_player.units.add((self.size, self.size))
        self.passive_player.reachable.update(
            self.get_adjacent_cells(self.size, self.size)
        )

    def make_turn(self, x, y):
        cell = x, y
        if cell not in self.active_player.reachable:
            return False

        if cell in self.passive_player.units:
            self.passive_player.units.remove(cell)
            self.active_player.walls.add(cell)
            self._rebuild_reachable_set(self.passive_player, self.active_player)
        else:
            self.active_player.units.add(cell)

        self._rebuild_reachable_set(self.active_player, self.passive_player)
        self._decrement_turns()

        return True

    def get_adjacent_cells(self, x, y):
        for x_ in (x - 1, x, x + 1):
            for y_ in (y - 1, y, y + 1):
                if self.is_valid_cell(x_, y_) and (x_ != x or y_ != y):
                    yield x_, y_

    def is_valid_cell(self, x, y):
        return 1 <= x <= self.size and 1 <= y <= self.size

    def _rebuild_reachable_set(self, player, opponent):
        player.reachable.clear()
        sources = player.units.copy()
        while True:
            new_sources = set()
            for x, y in sources:
                for cell in self.get_adjacent_cells(x, y):
                    if cell in sources:
                        continue
                    if cell in player.walls:
                        new_sources.add(cell)
                    elif cell not in opponent.walls and cell not in player.units:
                        player.reachable.add(cell)
            if not new_sources:
                break
            sources.update(new_sources)

    def _decrement_turns(self):
        self.turns_left -= 1
        if not self.turns_left:
            self.active_player, self.passive_player = (
                self.passive_player,
                self.active_player,
            )
            self.turns_left = 3

    def __str__(self):
        board = [[" " for j in range(self.size)] for i in range(self.size)]
        for x, y in self.active_player.units:
            board[x - 1][y - 1] = "o"
        for x, y in self.active_player.walls:
            board[x - 1][y - 1] = "O"
        for x, y in self.passive_player.units:
            board[x - 1][y - 1] = "x"
        for x, y in self.passive_player.walls:
            board[x - 1][y - 1] = "X"
        return "\n".join("".join(row) for row in board)
