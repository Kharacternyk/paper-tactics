def is_valid_cell(x, y):
    return 1 <= x <= 10 and 1 <= y <= 10


def adjacent_cells(x, y):
    for x_ in (x - 1, x, x + 1):
        for y_ in (y - 1, y, y + 1):
            if is_valid_cell(x_, y_) and (x_ != x or y_ != y):
                yield x_, y_


class Player:
    def __init__(self):
        self.units = set()
        self.walls = set()
        self.reachable = set()


class Game:
    def __init__(self):
        self.active_player = Player()
        self.active_player.units.add((1, 1))
        self.active_player.reachable.update(adjacent_cells(1, 1))

        self.passive_player = Player()
        self.passive_player.units.add((10, 10))
        self.passive_player.reachable.update(adjacent_cells(10, 10))

        self.turns_left = 3

    def make_turn(self, x, y):
        cell = x, y
        if cell not in self.active_player.reachable:
            return False

        if cell in self.passive_player.units:
            self.passive_player.units.remove(cell)
            self.active_player.walls.add(cell)
        else:
            self.active_player.units.add(cell)

        self.turns_left -= 1
        if not self.turns_left:
            self.active_player, self.passive_player = (
                self.passive_player,
                self.active_player,
            )
            self.turns_left = 3

        self._update_reachable_set()
        return True

    def _update_reachable_set(self):
        self.active_player.reachable.clear()
        sources = self.active_player.units.copy()
        while True:
            new_sources = set()
            for x, y in sources:
                for cell in adjacent_cells(x, y):
                    if cell in sources:
                        continue
                    if cell in self.active_player.walls:
                        new_sources.add(cell)
                    elif (
                        cell not in self.passive_player.walls
                        and cell not in self.active_player.units
                    ):
                        self.active_player.reachable.add(cell)
            if not new_sources:
                break
            sources.update(new_sources)

    def __str__(self):
        board = [[" " for j in range(10)] for i in range(10)]
        for x, y in self.active_player.units:
            board[x - 1][y - 1] = "*"
        for x, y in self.active_player.walls:
            board[x - 1][y - 1] = "#"
        for x, y in self.passive_player.units:
            board[x - 1][y - 1] = "o"
        for x, y in self.passive_player.walls:
            board[x - 1][y - 1] = "@"
        return "\n".join("".join(row) for row in board)
