import asyncio

from bidict import bidict
from websockets.exceptions import ConnectionClosed
from websockets.server import WebSocketServerProtocol

from paper_tactics.entities.game_view import GameView
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


class WebsocketsPlayerNotifier(PlayerNotifier):
    def __init__(self) -> None:
        self.websockets: bidict[str, WebSocketServerProtocol] = bidict()

    def send(self, player_id: str, message: str):
        try:
            asyncio.get_event_loop().run_until_complete(
                self.websockets[player_id].send(message)
            )
        except ConnectionClosed:
            del self.websockets[player_id]
            raise PlayerGoneException(player_id)
        except KeyError:
            raise PlayerGoneException(player_id)
