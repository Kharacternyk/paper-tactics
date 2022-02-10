from dataclasses import dataclass
from dataclasses import field
from uuid import uuid4

from paper_tactics.entities.cell import Cell


@dataclass
class Player:
    id: str = field(default_factory=lambda: uuid4().hex)
    units: set[Cell] = field(default_factory=set)
    walls: set[Cell] = field(default_factory=set)
    reachable: set[Cell] = field(default_factory=set)
    has_lost: bool = False
