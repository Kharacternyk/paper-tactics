from dataclasses import asdict
from typing import Any, Optional, cast

from paper_tactics.adapters.dynamodb_storage import DynamodbStorage
from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.ports.match_request_queue import MatchRequestQueue


class DynamodbMatchRequestQueue(MatchRequestQueue, DynamodbStorage):
    def put(self, request: MatchRequest) -> None:
        self._table.put_item(
            Item={
                self._key: request.id,
                self._ttl_key: self.get_expiration_time(),
                "view_data": request.view_data,
                "game_preferences": asdict(request.game_preferences)
                if request.game_preferences
                else None,
            }
        )

    def pop(
        self, game_preferences: Optional[GamePreferences]
    ) -> Optional[MatchRequest]:
        queue = self._table.scan(ConsistentRead=True)

        for i in range(queue["Count"]):
            item = queue["Items"][i]
            queued_preferences = self._parse_preferences(item["game_preferences"])
            if (
                queued_preferences == game_preferences
                or not game_preferences
                or not queued_preferences
            ):
                self._table.delete_item(Key={self._key: item[self._key]})
                return MatchRequest(
                    cast(str, item[self._key]),
                    cast(dict[str, str], item["view_data"]),
                    queued_preferences,
                )

    def _parse_preferences(self, item: Any) -> Optional[GamePreferences]:
        return (
            GamePreferences(
                **{
                    key: value
                    if isinstance(value, bool) or isinstance(value, str)
                    else int(value)
                    for key, value in item.items()
                }
            )
            if item
            else None
        )
