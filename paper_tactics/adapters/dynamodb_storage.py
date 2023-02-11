import boto3
from time import time


class DynamodbStorage:
    def __init__(self, table_name: str, key: str, ttl_key: str, ttl_in_seconds: int):
        self._key = key
        self._ttl_key = ttl_key
        self._ttl_in_seconds = ttl_in_seconds
        self._table = boto3.resource("dynamodb").Table(table_name)

    def get_expiration_time(self) -> int:
        now = int(time())

        return now + self._ttl_in_seconds
