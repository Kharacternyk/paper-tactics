import json
from typing import Any

import boto3

from paper_tactics.entities.game import Game
from paper_tactics.entities.player import Player
from paper_tactics.ports.player_notifier import PlayerGoneException
from paper_tactics.ports.player_notifier import PlayerNotifier


class AwsApiGatewayPlayerNotifier(PlayerNotifier):
    def __init__(self, endpoint_url: str):
        self._client = boto3.client(
            "apigatewaymanagementapi", endpoint_url=endpoint_url
        )

    def notify(self, player_id: str, game: Game) -> None:
        view = self._create_game_view(player_id, game)

        try:
            self._client.post_to_connection(
                Data=json.dumps(view, separators=(",", ":")).encode(),
                ConnectionId=player_id,
            )
        except self._client.exceptions.GoneException:
            raise PlayerGoneException(player_id)

    def _create_game_view(self, player_id: str, game: Game) -> dict[str, Any]:
        if player_id == game.active_player.id:
            return self._create_game_view_for_active_player(game)
        elif player_id == game.passive_player.id:
            return self._create_game_view_for_passive_player(game)

        raise ValueError("No such player")

    def _create_game_view_for_active_player(self, game: Game) -> dict[str, Any]:
        return {
            "id": game.id,
            "size": game.size,
            "myTurn": True,
            "turnsLeft": game.turns_left,
            "me": self._create_player_view(game.active_player),
            "opponent": self._create_player_view(game.passive_player),
        }

    def _create_game_view_for_passive_player(self, game: Game) -> dict[str, Any]:
        return {
            "id": game.id,
            "size": game.size,
            "myTurn": False,
            "turnsLeft": game.turns_left,
            "me": self._create_player_view(game.passive_player),
            "opponent": self._create_player_view(game.active_player),
        }

    def _create_player_view(self, player: Player) -> dict[str, Any]:
        return {
            "units": list(player.units),
            "walls": list(player.walls),
            "reachable": list(player.reachable),
            "isGone": player.is_gone,
            "isDefeated": player.is_defeated,
            "viewData": player.view_data,
        }
