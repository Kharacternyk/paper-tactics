import asyncio

from bidict import bidict
from websockets.exceptions import ConnectionClosed
from websockets.server import WebSocketServerProtocol

from paper_tactics.entities.game import Game
from paper_tactics.entities.game_view import GameView
from paper_tactics.ports.player_notifier import PlayerGoneException, PlayerNotifier


class WebsocketsPlayerNotifier(PlayerNotifier):
    def __init__(self) -> None:
        self.websockets: bidict[str, WebSocketServerProtocol] = bidict()

    def notify(self, player_id: str, game: Game) -> None:
        view = GameView(game, player_id)

        try:
            asyncio.get_event_loop().run_until_complete(
                self.websockets[player_id].send(view.to_json())
            )
        except ConnectionClosed:
            del self.websockets[player_id]
            raise PlayerGoneException(player_id)
        except KeyError:
            raise PlayerGoneException(player_id)
