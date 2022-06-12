from dataclasses import dataclass


@dataclass(frozen=True)
class GamePreferences:
    size: int = 10
    turn_count: int = 3
    is_visibility_applied: bool = False

    @property
    def valid(self) -> bool:
        return 2 <= self.size <= 12 and 1 <= self.turn_count <= 7
