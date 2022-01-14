import json
import traceback

import boto3


def lambda_handler(handler):
    resources = Resources()

    def decorated_handler(event_dict, context):
        event = Event(event_dict)
        resources.event_dict = event_dict

        try:
            handler(event, resources)
        except Exception:
            print("EXCEPTION:", traceback.format_exc())

        return {"statusCode": 200}

    return decorated_handler


class Cacheable:
    def __init__(self):
        self._cache = {}

    def get(self, resource, init):
        if resource not in self._cache:
            self._cache[resource] = init()
        return self._cache[resource]


class Event(Cacheable):
    def __init__(self, event_dict):
        super().__init__()
        self._event_dict = event_dict

    @property
    def connection_id(self):
        return self._event_dict["requestContext"]["connectionId"]

    @property
    def game_id(self):
        return self._body["gameId"]

    @property
    def cell(self):
        def get_cell():
            cell = self._body["cell"]
            assert len(cell) == 2
            return cell

        return self.get("cell", get_cell)

    @property
    def _body(self):
        return self.get("body", lambda: json.loads(self._event_dict["body"]))


class Resources(Cacheable):
    def __init__(self):
        super().__init__()
        self.event_dict = {}

    @property
    def connection_manager(self):
        return self.get(
            "connection_manager",
            lambda: ConnectionManager(
                "https://"
                + self.event_dict["requestContext"]["domainName"]
                + "/"
                + self.event_dict["requestContext"]["stage"]
            ),
        )

    @property
    def queue_table(self):
        return self.get(
            "queue_table", lambda: self._dynamodb.Table("paper-tactics-client-queue")
        )

    @property
    def games_table(self):
        return self.get(
            "games_table", lambda: self._dynamodb.Table("paper-tactics-game-states")
        )

    @property
    def _dynamodb(self):
        return self.get("dynamodb", lambda: boto3.resource("dynamodb"))


class ConnectionManager:
    def __init__(self, url):
        self._client = boto3.client("apigatewaymanagementapi", endpoint_url=url)
        self.GoneException = self._client.exceptions.GoneException

    def send(self, connection_id, data: dict):
        self._client.post_to_connection(
            Data=json.dumps(data, separators=(",", ":")).encode(),
            ConnectionId=connection_id,
        )
