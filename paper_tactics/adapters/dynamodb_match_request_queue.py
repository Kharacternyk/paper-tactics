from time import time
from typing import Optional

import boto3

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
            }
        )

    def pop(self) -> Optional[MatchRequest]:
        queue = self._table.scan(ConsistentRead=True)

        if not queue["Count"]:
            return None

        item = queue["Items"][0]
        self._table.delete_item(Key={self._key: item[self._key]})

        return MatchRequest(item[self._key], item["view_data"])

    def _get_expiration_time(self):
        now = int(time())

        return now + self._ttl_in_seconds
