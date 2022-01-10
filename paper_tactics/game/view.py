def create_game_view(game, player_id):
    if player_id == game.active_player_id:
        return create_game_view_for_active_player(game)
    elif player_id == game.passive_player_id:
        return create_game_view_for_passive_player(game)
    else:
        return create_empty_view()


def create_game_view_for_active_player(game):
    return {
        "game-id": game.id,
        "my-player-id": game.active_player.id,
        "my-turn": True,
        "turns-left": game.turns_left,
        "me": _create_player_view(game.active_player),
        "opponent": _create_player_view(game.passive_player),
    }


def create_game_view_for_passive_player(game):
    return {
        "game-id": game.id,
        "my-player-id": game.passive_player.id,
        "my-turn": False,
        "turns-left": game.turns_left,
        "me": _create_player_view(game.passive_player),
        "opponent": _create_player_view(game.active_player),
    }


def create_empty_view():
    return {}


def _create_player_view(player):
    return {
        "units": list(player.units),
        "walls": list(player.walls),
        "reachable": list(player.reachable),
    }
