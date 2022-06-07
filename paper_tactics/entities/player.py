from dataclasses import dataclass, field

from paper_tactics.entities.cell import Cell


@dataclass
class Player:
    id: str = ""
    units: set[Cell] = field(default_factory=set)
    walls: set[Cell] = field(default_factory=set)
    reachable: set[Cell] = field(default_factory=set)
    visible: set[Cell] = field(default_factory=set)
    view_data: dict[str, str] = field(default_factory=dict)
    is_gone: bool = False
    is_defeated: bool = False
