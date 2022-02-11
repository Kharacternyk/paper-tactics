from abc import ABC
from abc import abstractmethod
from typing import Optional

from paper_tactics.entities.match_request import MatchRequest


class MatchRequestQueue(ABC):
    @abstractmethod
    def put(self, request: MatchRequest) -> None:
        ...

    @abstractmethod
    def pop(self) -> Optional[MatchRequest]:
        ...
