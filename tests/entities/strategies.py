from dataclasses import replace

from hypothesis.strategies import booleans, composite, dictionaries, integers, text

from paper_tactics.entities.game import Game
from paper_tactics.entities.game_preferences import GamePreferences
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.entities.player import Player


@composite
def game_preferences(
    draw, is_against_bot=None, is_visibility_applied=None
) -> GamePreferences:
    return GamePreferences(
        size=draw(integers(min_value=2, max_value=7)),
        turn_count=draw(integers(min_value=2, max_value=5)),
        is_visibility_applied=draw(booleans())
        if is_visibility_applied is None
        else is_visibility_applied,
        is_against_bot=draw(booleans()) if is_against_bot is None else is_against_bot,
    )


@composite
def match_requests(draw) -> MatchRequest:
    return MatchRequest(
        id=draw(text(min_size=1)),
        view_data=draw(dictionaries(text(), text())),
        game_preferences=draw(game_preferences()),
    )


@composite
def players(draw) -> Player:
    return Player(draw(text(min_size=1)), view_data=draw(dictionaries(text(), text())))


@composite
def games(draw, shallow=False, is_visibility_applied=None, is_against_bot=None) -> Game:
    preferences = draw(
        game_preferences(
            is_against_bot=is_against_bot, is_visibility_applied=is_visibility_applied
        )
    )
    turn_number = draw(integers(min_value=0, max_value=preferences.size ** 2 * 2))

    if shallow:
        game = Game(
            preferences=preferences,
            active_player=Player("a"),
            passive_player=Player("b"),
        )
    else:
        active_player = draw(players())
        passive_player = draw(players())
        game = Game(
            preferences=preferences,
            id=draw(text(min_size=1)),
            active_player=active_player,
            passive_player=replace(passive_player, id="*" + active_player.id)
            if active_player.id == passive_player.id
            else passive_player,
        )

    game.init_players()

    for i in range(turn_number):
        if not game.active_player.can_win or not game.passive_player.can_win:
            break

        reachable = list(game.active_player.reachable)
        turn = reachable[draw(integers(min_value=0, max_value=len(reachable) - 1))]
        game.make_turn(game.active_player.id, turn)

    return game
