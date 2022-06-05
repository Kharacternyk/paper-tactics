import asyncio
import json
from typing import Any

from bidict import bidict
from websockets.exceptions import ConnectionClosed
from websockets.server import WebSocketServerProtocol

from paper_tactics.entities.game import Game
from paper_tactics.entities.player import Player
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


class WebsocketsPlayerNotifier(PlayerNotifier):
    def __init__(self) -> None:
        self.websockets: bidict[str, WebSocketServerProtocol] = bidict()

    def notify(self, player_id: str, game: Game) -> None:
        view = self._create_game_view(player_id, game)

        try:
            asyncio.get_event_loop().run_until_complete(
                self.websockets[player_id].send(json.dumps(view))
            )
        except ConnectionClosed:
            del self.websockets[player_id]
            raise PlayerGoneException(player_id)
        except KeyError:
            raise PlayerGoneException(player_id)

    # TODO the following methods are identical to the
    # AwsApiGatewayPlayerNotifer ones and should be moved to the entity level.
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
