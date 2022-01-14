def create_game_view(game, player_id):
    if player_id == game.active_player.id:
        return create_game_view_for_active_player(game)
    elif player_id == game.passive_player.id:
        return create_game_view_for_passive_player(game)

    raise ValueError("No such player")


def create_game_view_for_active_player(game):
    return {
        "gameId": game.id,
        "myTurn": True,
        "turnsLeft": game.turns_left,
        "me": _create_player_view(game.active_player),
        "opponent": _create_player_view(game.passive_player),
    }


def create_game_view_for_passive_player(game):
    return {
        "gameId": game.id,
        "myTurn": False,
        "turnsLeft": game.turns_left,
        "me": _create_player_view(game.passive_player),
        "opponent": _create_player_view(game.active_player),
    }


def _create_player_view(player):
    return {
        "units": list(player.units),
        "walls": list(player.walls),
        "reachable": list(player.reachable),
    }
