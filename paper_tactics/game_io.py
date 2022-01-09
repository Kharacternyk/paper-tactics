from paper_tactics.game import Game
from paper_tactics.game import Player


def serialize_to_dynamodb_dict(game):
    def serialize_player(player):
        return {
            "id": player.id,
            "units": list(player.units),
            "walls": list(player.walls),
            "reachable": list(player.reachable),
        }

    return {
        "id": game.id,
        "size": game.size,
        "turns-left": game.turns_left,
        "active-player": serialize_player(game.active_player),
        "passive-player": serialize_player(game.passive_player),
    }


def deserialize_from_dynamodb_dict(source):
    def deserialize_player(source):
        return Player(
            id=source["id"],
            units=set(source["units"]),
            walls=set(source["walls"]),
            reachable=set(source["reachable"]),
        )

    return Game(
        id=source["id"],
        size=source["size"],
        turns_left=source["turns-left"],
        active_player=deserialize_player(source["active-player"]),
        passive_player=deserialize_player(source["passive-player"]),
    )
