from dataclasses import dataclass


@dataclass(frozen=True)
class GamePreferences:
    size: int = 10
    turn_count: int = 3
    is_visibility_applied: bool = False
    is_against_bot: bool = False
    trench_density_percent: int = 0

    @property
    def valid(self) -> bool:
        return (
            isinstance(self.size, int)
            and isinstance(self.turn_count, int)
            and isinstance(self.trench_density_percent, int)
            and 3 <= self.size <= 12
            and 1 <= self.turn_count <= 7
            and 0 <= self.trench_density_percent <= 100
        )
