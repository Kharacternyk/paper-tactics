import asyncio
import json
from typing import cast
from uuid import uuid4

import nest_asyncio
from websockets.server import WebSocketServerProtocol, serve

from paper_tactics.adapters.in_memory_game_repository import InMemoryGameRepository
from paper_tactics.adapters.in_memory_match_request_queue import (
    InMemoryMatchRequestQueue,
)
from paper_tactics.adapters.stdout_logger import StdoutLogger
from paper_tactics.adapters.websockets_player_notifier import WebsocketsPlayerNotifier
from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.use_cases.concede import concede
from paper_tactics.use_cases.create_game import create_game
from paper_tactics.use_cases.make_turn import make_turn

nest_asyncio.apply()

game_repository = InMemoryGameRepository()
match_request_queue = InMemoryMatchRequestQueue()
player_notifier = WebsocketsPlayerNotifier()
logger = StdoutLogger()


async def handler(websocket: WebSocketServerProtocol) -> None:
    async for message in websocket:
        try:
            event = json.loads(message)
        except json.JSONDecodeError as e:
            logger.log_exception(e)
            return

        if event.get("action") == "create-game":
            preferences = GamePreferences(**event.get("preferences", {}))
            request = MatchRequest(uuid4().hex, event.get("view_data", {}), preferences)
            player_notifier.websockets[request.id] = websocket
            create_game(
                game_repository, match_request_queue, player_notifier, logger, request
            )
        elif event.get("action") == "make-turn":
            try:
                player_id = player_notifier.websockets.inverse[websocket]
                game_id = event["gameId"]
                cell = cast(Cell, tuple(event["cell"]))
                assert len(cell) == 2
            except Exception as e:
                logger.log_exception(e)
                return
            make_turn(
                game_repository, player_notifier, logger, game_id, player_id, cell
            )
        elif event.get("action") == "concede":
            try:
                player_id = player_notifier.websockets.inverse[websocket]
                game_id = event["gameId"]
            except Exception as e:
                logger.log_exception(e)
                return
            concede(game_repository, player_notifier, logger, game_id, player_id)


async def main() -> None:
    async with serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
