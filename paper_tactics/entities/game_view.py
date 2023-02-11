from dataclasses import dataclass

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.player_view import PlayerView
from paper_tactics.entities.game_preferences import GamePreferences


@dataclass(frozen=True)
class GameView:
    id: str
    turns_left: int
    my_turn: bool
    me: PlayerView
    opponent: PlayerView
    trenches: frozenset[Cell]
    preferences: GamePreferences
