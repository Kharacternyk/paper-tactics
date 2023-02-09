from dataclasses import asdict
from time import time
from typing import Any, Optional, cast

import boto3

from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.ports.match_request_queue import MatchRequestQueue


class DynamodbMatchRequestQueue(MatchRequestQueue):
    def __init__(self, table_name: str, key: str, ttl_key: str, ttl_in_seconds: int):
        self._key = key
        self._ttl_key = ttl_key
        self._ttl_in_seconds = ttl_in_seconds
        self._table = boto3.resource("dynamodb").Table(table_name)

    def put(self, request: MatchRequest) -> None:
        self._table.put_item(
            Item={
                self._key: request.id,
                self._ttl_key: self._get_expiration_time(),
                "view_data": request.view_data,
                "game_preferences": asdict(request.game_preferences),
            }
        )

    def pop(self, game_preferences: GamePreferences) -> Optional[MatchRequest]:
        queue = self._table.scan(ConsistentRead=True)

        for i in range(queue["Count"]):
            item = queue["Items"][i]
            queued_preferences = self._parse_preferences(item["game_preferences"])
            if queued_preferences == game_preferences:
                self._table.delete_item(Key={self._key: item[self._key]})
                return MatchRequest(
                    cast(str, item[self._key]),
                    cast(dict[str, str], item["view_data"]),
                    game_preferences,
                )

        return None

    def _parse_preferences(self, item: Any) -> GamePreferences:
        return GamePreferences(
            int(item["size"]),
            int(item["turn_count"]),
            item["is_visibility_applied"],
            item["is_against_bot"],
            int(item["trench_density_percent"]),
        )

    def _get_expiration_time(self) -> int:
        now = int(time())

        return now + self._ttl_in_seconds
