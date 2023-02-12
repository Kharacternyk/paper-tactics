from dataclasses import asdict
from typing import Any, Iterable

import boto3
from paper_tactics.adapters.dynamodb_storage import DynamodbStorage
from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game import Game
from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.player import Player
from paper_tactics.ports.game_repository import GameRepository, NoSuchGameException


class DynamodbGameRepository(GameRepository, DynamodbStorage):
    def store(self, game: Game) -> None:
        serialized_game: dict[str, Any] = {
            self._key: game.id,
            "turns-left": game.turns_left,
            "active-player": self._serialize_player(game.active_player),
            "passive-player": self._serialize_player(game.passive_player),
            "preferences": asdict(game.preferences),
            "trenches": list(game.trenches),
            self._ttl_key: self.get_expiration_time(),
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
                **{
                    key: value if isinstance(value, bool) else int(value)
                    for key, value in serialized_game["preferences"].items()
                }
            ),
            trenches=frozenset(
                (int(x), int(y)) for x, y in serialized_game["trenches"]
            ),
        )

    def _serialize_player(self, player: Player) -> dict[str, Any]:
        return {
            "id": player.id,
            "units": list(player.units),
            "walls": list(player.walls),
            "reachable": list(player.reachable),
            "visible_opponent": list(player.visible_opponent),
            "visible_terrain": list(player.visible_terrain),
            "is_gone": player.is_gone,
            "is_defeated": player.is_defeated,
            "view_data": player.view_data,
        }

    def _deserialize_player(self, source: dict[str, Any]) -> Player:
        return Player(
            id=source["id"],
            units=self._deserialize_cells(source["units"]),
            walls=self._deserialize_cells(source["walls"]),
            reachable=self._deserialize_cells(source["reachable"]),
            visible_opponent=self._deserialize_cells(source["visible_opponent"]),
            visible_terrain=self._deserialize_cells(source["visible_terrain"]),
            is_gone=source["is_gone"],
            is_defeated=source["is_defeated"],
            view_data=source["view_data"],
        )

    def _deserialize_cells(self, cells: Iterable[Cell]) -> set[Cell]:
        return set((int(x), int(y)) for x, y in cells)
