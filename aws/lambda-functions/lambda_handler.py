import json

import boto3


def lambda_handler(handler):
    def decorated_handler(event_dict, context):
        event = Event(event_dict)
        resources = Resources(event_dict)

        handler(event, resources)

        return {"statusCode": 200}

    return decorated_handler


class Event:
    def __init__(self, event_dict):
        self.connection_id = event_dict["requestContext"]["connectionId"]


class Resources:
    def __init__(self, event_dict):
        self._event_dict = event_dict
        self._cache = {}

    @property
    def connection_manager(self):
        url = (
            "https://"
            + self._event_dict["requestContext"]["domainName"]
            + "/"
            + self._event_dict["requestContext"]["stage"]
        )

        return self._get("connection_manager", lambda: ConnectionManager(url))

    @property
    def queue_table(self):
        return self._get(
            "queue_table", lambda: self._dynamodb.Table("paper-tactics-client-queue")
        )

    @property
    def games_table(self):
        return self._get(
            "games_table", lambda: self._dynamodb.Table("paper-tactics-game-states")
        )

    @property
    def _dynamodb(self):
        return self._get("dynamodb", lambda: boto3.resource("dynamodb"))

    def _get(self, resource, init):
        if resource not in self._cache:
            self._cache[resource] = init()
        return self._cache[resource]


class ConnectionManager:
    def __init__(self, url):
        self._client = boto3.client("apigatewaymanagementapi", endpoint_url=url)
        self.GoneException = self._client.exceptions.GoneException

    def send(self, connection_id, data: dict):
        self._client.post_to_connection(
            Data=json.dumps(data, separators=(",", ":")).encode(),
            ConnectionId=connection_id,
        )
