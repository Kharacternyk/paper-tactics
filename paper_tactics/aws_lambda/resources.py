import json

import boto3

from paper_tactics.on_demand_dict import OnDemandDict


class LambdaResources(OnDemandDict):
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
