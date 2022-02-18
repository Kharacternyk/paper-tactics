from __future__ import annotations

import json
from typing import Optional

from redis import Redis

from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.ports.match_request_queue import MatchRequestQueue


class RedisMatchRequestQueue(MatchRequestQueue):
    def __init__(self, server: Redis[str], key: str):
        self._server = server
        self._key = key

    def put(self, request: MatchRequest) -> None:
        self._server.lpush(self._key, json.dumps(request.view_data), request.id)

    def pop(self) -> Optional[MatchRequest]:
        queue_head = self._server.lpop(self._key, 2)

        if queue_head and len(queue_head) == 2:
            id, serialized_view_data = queue_head
            view_data = json.loads(serialized_view_data)
            return MatchRequest(id, view_data)

        return None
