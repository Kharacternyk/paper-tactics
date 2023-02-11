from typing import Iterable

from dataclasses import dataclass

from paper_tactics.entities.cell import Cell


@dataclass(frozen=True)
class GamePreferences:
    size: int = 10
    turn_count: int = 3
    is_visibility_applied: bool = False
    is_against_bot: bool = False
    trench_density_percent: int = 0

    @property
    def valid(self) -> bool:
        return (
            isinstance(self.size, int)
            and isinstance(self.turn_count, int)
            and isinstance(self.trench_density_percent, int)
            and 3 <= self.size <= 12
            and 1 <= self.turn_count <= 7
            and 0 <= self.trench_density_percent <= 100
        )

    def is_valid_cell(self, cell: Cell) -> bool:
        x, y = cell
        return 1 <= x <= self.size and 1 <= y <= self.size

    def get_symmetric_cell(self, cell: Cell) -> Cell:
        x, y = cell
        s = self.size + 1
        return s - x, s - y

    def get_adjacent_cells(self, cell: Cell) -> Iterable[Cell]:
        x, y = cell
        for x_ in (x - 1, x, x + 1):
            for y_ in (y - 1, y, y + 1):
                if self.is_valid_cell((x_, y_)) and (x_ != x or y_ != y):
                    yield x_, y_
