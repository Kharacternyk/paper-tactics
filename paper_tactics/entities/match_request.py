from dataclasses import dataclass, field
from typing import Optional

from paper_tactics.entities.game_preferences import GamePreferences


@dataclass(frozen=True)
class MatchRequest:
    id: str = ""
    view_data: dict[str, str] = field(default_factory=dict)
    game_preferences: Optional[GamePreferences] = None
