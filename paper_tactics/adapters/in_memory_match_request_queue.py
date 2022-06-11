from typing import Optional

from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.ports.match_request_queue import MatchRequestQueue


class InMemoryMatchRequestQueue(MatchRequestQueue):
    def __init__(self) -> None:
        self._match_requests: list[MatchRequest] = []

    def put(self, request: MatchRequest) -> None:
        self._match_requests.append(request)

    def pop(self, game_preferences: GamePreferences) -> Optional[MatchRequest]:
        queued_request = next(
            (
                request
                for request in self._match_requests
                if request.game_preferences == game_preferences
            ),
            None,
        )
        if queued_request:
            self._match_requests.remove(queued_request)
        return queued_request
