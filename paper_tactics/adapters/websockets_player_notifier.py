import asyncio
from dataclasses import asdict
import json

from bidict import bidict
from websockets.exceptions import ConnectionClosed
from websockets.server import WebSocketServerProtocol

from paper_tactics.entities.game_view import GameView
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


class WebsocketsPlayerNotifier(PlayerNotifier):
    def __init__(self) -> None:
        self.websockets: bidict[str, WebSocketServerProtocol] = bidict()

    def notify(self, player_id: str, game_view: GameView) -> None:
        try:
            asyncio.get_event_loop().run_until_complete(
                self.websockets[player_id].send(
                    json.dumps(asdict(game_view), default=list)
                )
            )
        except ConnectionClosed:
            del self.websockets[player_id]
            raise PlayerGoneException(player_id)
        except KeyError:
            raise PlayerGoneException(player_id)
