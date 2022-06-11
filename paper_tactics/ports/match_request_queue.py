from abc import ABC, abstractmethod
from typing import Optional

from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.match_request import MatchRequest


class MatchRequestQueue(ABC):
    @abstractmethod
    def put(self, request: MatchRequest) -> None:
        ...

    @abstractmethod
    def pop(self, game_preferences: GamePreferences) -> Optional[MatchRequest]:
        ...
