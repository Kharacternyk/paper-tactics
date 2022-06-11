from dataclasses import dataclass

from paper_tactics.entities.cell import Cell


@dataclass(frozen=True)
class PlayerView:
    units: frozenset[Cell]
    walls: frozenset[Cell]
    reachable: frozenset[Cell]
    view_data: dict[str, str]
    is_gone: bool
    is_defeated: bool
