from dataclasses import asdict
import json

import boto3

from paper_tactics.entities.game import Game
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


class AwsApiGatewayPlayerNotifier(PlayerNotifier):
    def __init__(self, endpoint_url: str):
        self._client = boto3.client(
            "apigatewaymanagementapi", endpoint_url=endpoint_url
        )

    def notify(self, player_id: str, game: Game) -> None:
        if not player_id:
            return

        view = game.get_view(player_id)

        try:
            self._client.post_to_connection(
                Data=json.dumps(asdict(view), default=list),
                ConnectionId=player_id,
            )
        except self._client.exceptions.GoneException:
            raise PlayerGoneException(player_id)
