from time import time

from paper_tactics.game.model import Game
from paper_tactics.game.model import Player


def serialize(game):
    return {
        "id": game.id,
        "size": game.size,
        "turns-left": game.turns_left,
        "active-player": _serialize_player(game.active_player),
        "passive-player": _serialize_player(game.passive_player),
        "expiration-time": _get_expiration_time(),
    }


def deserialize(source):
    return Game(
        id=source["id"],
        size=source["size"],
        turns_left=source["turns-left"],
        active_player=_deserialize_player(source["active-player"]),
        passive_player=_deserialize_player(source["passive-player"]),
    )


def _serialize_player(player):
    return {
        "id": player.id,
        "units": list(player.units),
        "walls": list(player.walls),
        "reachable": list(player.reachable),
    }


def _deserialize_player(source):
    return Player(
        id=source["id"],
        units=set(source["units"]),
        walls=set(source["walls"]),
        reachable=set(source["reachable"]),
    )


def _get_expiration_time():
    now = int(time())
    ten_minutes = 600

    return now + ten_minutes
