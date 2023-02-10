from dataclasses import dataclass, field
from typing import Final

from paper_tactics.entities.cell import Cell


@dataclass
class Player:
    id: Final[str] = ""
    units: set[Cell] = field(default_factory=set)
    walls: set[Cell] = field(default_factory=set)
    reachable: set[Cell] = field(default_factory=set)
    visible_opponent: set[Cell] = field(default_factory=set)
    visible_terrain: set[Cell] = field(default_factory=set)
    view_data: Final[dict[str, str]] = field(default_factory=dict)
    is_gone: bool = False
    is_defeated: bool = False

    @property
    def can_win(self) -> bool:
        return not self.is_defeated and not self.is_gone
