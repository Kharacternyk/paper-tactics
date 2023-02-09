from dataclasses import asdict
from time import time
from typing import Any
from decimal import Decimal

import boto3

from paper_tactics.entities.game import Game
from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.player import Player
from paper_tactics.ports.game_repository import GameRepository, NoSuchGameException


class DynamodbGameRepository(GameRepository):
    def __init__(self, table_name: str, key: str, ttl_key: str, ttl_in_seconds: int):
        self._key = key
        self._ttl_key = ttl_key
        self._ttl_in_seconds = ttl_in_seconds
        self._table = boto3.resource("dynamodb").Table(table_name)

    def store(self, game: Game) -> None:
        serialized_game: dict[str, Any] = {
            self._key: game.id,
            "turns-left": game.turns_left,
            "active-player": self._serialize_player(game.active_player),
            "passive-player": self._serialize_player(game.passive_player),
            "preferences": asdict(game.preferences),
            "trenches": list(game.trenches),
            self._ttl_key: self._get_expiration_time(),
        }

        self._table.put_item(Item=serialized_game)

    def fetch(self, game_id: str) -> Game:
        try:
            serialized_game: dict[str, Any] = self._table.get_item(
                Key={self._key: game_id}, ConsistentRead=True
            )["Item"]
        except KeyError:
            raise NoSuchGameException(game_id)

        return Game(
            id=serialized_game[self._key],
            turns_left=int(serialized_game["turns-left"]),
            active_player=self._deserialize_player(serialized_game["active-player"]),
            passive_player=self._deserialize_player(serialized_game["passive-player"]),
            preferences=GamePreferences(
                int(serialized_game["preferences"]["size"]),
                int(serialized_game["preferences"]["turn_count"]),
                serialized_game["preferences"]["is_visibility_applied"],
                serialized_game["preferences"]["is_against_bot"],
                int(serialized_game["preferences"]["trench_density_percent"]),
            ),
            trenches=frozenset(serialized_game["trenches"]),
        )

    def _serialize_player(self, player: Player) -> dict[str, Any]:
        return {
            "id": player.id,
            "units": list(player.units),
            "walls": list(player.walls),
            "reachable": list(player.reachable),
            "visible": list(player.visible),
            "is_gone": player.is_gone,
            "is_defeated": player.is_defeated,
            "view_data": player.view_data,
        }

    def _deserialize_player(self, source: dict[str, Any]) -> Player:
        return Player(
            id=source["id"],
            units=set((int(x), int(y)) for x, y in source["units"]),
            walls=set((int(x), int(y)) for x, y in source["walls"]),
            reachable=set((int(x), int(y)) for x, y in source["reachable"]),
            visible=set((int(x), int(y)) for x, y in source["visible"]),
            is_gone=source["is_gone"],
            is_defeated=source["is_defeated"],
            view_data=source["view_data"],
        )

    def _get_expiration_time(self) -> int:
        now = int(time())

        return now + self._ttl_in_seconds
