from time import time
from typing import Hashable
from typing import Optional

import boto3

from paper_tactics.ports.player_queue import PlayerQueue


class DynamodbPlayerQueue(PlayerQueue):
    def __init__(self, table_name: str, key: str, ttl_key: str, ttl_in_seconds: int):
        self._key = key
        self._ttl_key = ttl_key
        self._ttl_in_seconds = ttl_in_seconds
        self._table = boto3.resource("dynamodb").Table(table_name)

    def put(self, player_id: Hashable) -> None:
        self._table.put_item(
            Item={self._key: player_id, self._ttl_key: self._get_expiration_time()}
        )

    def pop(self) -> Optional[Hashable]:
        queue = self._table.scan(ConsistentRead=True)

        if not queue["Count"]:
            return None

        player_id = queue["Items"][0][self._key]
        self._table.delete_item(Key={self._key: player_id})

        return player_id

    def _get_expiration_time(self):
        now = int(time())

        return now + self._ttl_in_seconds
