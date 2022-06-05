from typing import Optional

from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.ports.match_request_queue import MatchRequestQueue


class InMemoryMatchRequestQueue(MatchRequestQueue):
    def __init__(self) -> None:
        self._match_request: Optional[MatchRequest] = None

    def put(self, request: MatchRequest) -> None:
        self._match_request = request

    def pop(self) -> Optional[MatchRequest]:
        queue_head = self._match_request
        self._match_request = None
        return queue_head
