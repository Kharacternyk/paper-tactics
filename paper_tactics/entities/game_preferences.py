from dataclasses import dataclass


@dataclass(frozen=True)
class GamePreferences:
    size: int = 10
    turn_count: int = 3
    is_visibility_applied: bool = False
