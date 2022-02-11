from dataclasses import dataclass
from dataclasses import field

from paper_tactics.entities.cell import Cell


@dataclass
class Player:
    id: str = ""
    units: set[Cell] = field(default_factory=set)
    walls: set[Cell] = field(default_factory=set)
    reachable: set[Cell] = field(default_factory=set)
    has_lost: bool = False
    view_data: dict[str, str] = field(default_factory=dict)
