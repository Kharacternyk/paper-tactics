import boto3

from paper_tactics.entities.game_view import GameView
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


class AwsApiGatewayPlayerNotifier(PlayerNotifier):
    def __init__(self, endpoint_url: str):
        self._client = boto3.client(
            "apigatewaymanagementapi", endpoint_url=endpoint_url
        )

    def send(self, player_id: str, message: str) -> None:
        try:
            self._client.post_to_connection(
                Data=message,
                ConnectionId=player_id,
            )
        except self._client.exceptions.GoneException:
            raise PlayerGoneException(player_id)
