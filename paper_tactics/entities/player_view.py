from dataclasses import dataclass

from paper_tactics.entities.cell import Cell


@dataclass
class PlayerView:
    units: set[Cell]
    walls: set[Cell]
    reachable: set[Cell]
    view_data: dict[str, str]
    is_gone: bool
    is_defeated: bool
