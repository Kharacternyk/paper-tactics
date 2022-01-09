from time import time

from paper_tactics.game import Game
from paper_tactics.game import Player


def serialize_to_dynamodb_dict(game):
    return {
        "id": game.id,
        "size": game.size,
        "turns-left": game.turns_left,
        "active-player": serialize_player_to_dynamodb_dict(game.active_player),
        "passive-player": serialize_player_to_dynamodb_dict(game.passive_player),
        "expiration-time": get_expiration_time(),
    }


def deserialize_from_dynamodb_dict(source):
    return Game(
        id=source["id"],
        size=source["size"],
        turns_left=source["turns-left"],
        active_player=deserialize_player_from_dynamodb_dict(source["active-player"]),
        passive_player=deserialize_player_from_dynamodb_dict(source["passive-player"]),
    )


def serialize_player_to_dynamodb_dict(player):
    return {
        "id": player.id,
        "units": list(player.units),
        "walls": list(player.walls),
        "reachable": list(player.reachable),
    }


def deserialize_player_from_dynamodb_dict(source):
    return Player(
        id=source["id"],
        units=set(source["units"]),
        walls=set(source["walls"]),
        reachable=set(source["reachable"]),
    )


def get_expiration_time():
    now = int(time())
    ten_minutes = 600

    return now + ten_minutes
