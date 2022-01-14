from lambda_handler import Event
from lambda_handler import lambda_handler
from lambda_handler import Resources

from paper_tactics.game.serialization.dynamodb import deserialize
from paper_tactics.game.serialization.dynamodb import serialize
from paper_tactics.game.view import create_game_view


@lambda_handler
def handler(event: Event, resources: Resources):
    serialized_game = resources.games_table.get_item(Key={"id": event.game_id})["Item"]
    game = deserialize(serialized_game)

    game.make_turn(*event.cell)

    try:
        resources.connection_manager.send(
            game.passive_player.id, create_game_view(game, game.passive_player.id)
        )
    except resources.connection_manager.GoneException:
        game.passive_player.reachable = set()

    try:
        resources.connection_manager.send(
            game.active_player.id, create_game_view(game, game.active_player.id)
        )
    except resources.connection_manager.GoneException:
        game.active_player.reachable = set()

    resources.games_table.put_item(Item=serialize(game))
