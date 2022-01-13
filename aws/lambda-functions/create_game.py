from lambda_handler import Event
from lambda_handler import lambda_handler
from lambda_handler import Resources

from paper_tactics.game.model import Game
from paper_tactics.game.serialization.dynamodb import serialize
from paper_tactics.game.view import create_game_view_for_active_player
from paper_tactics.game.view import create_game_view_for_passive_player


@lambda_handler
def handler(event: Event, resources: Resources):
    queue = resources.queue_table.scan(ConsistentRead=True)

    if queue["Count"]:
        queued_connection_id = queue["Items"][0]["connection-id"]
        game = Game()
        game.init_players()
        active_player_view = create_game_view_for_active_player(game)
        passive_player_view = create_game_view_for_passive_player(game)

        try:
            resources.connection_manager.send(queued_connection_id, active_player_view)
        except resources.connection_manager.GoneException:
            resources.queue_table.put_item(Item={"connection-id": event.connection_id})
        else:
            resources.connection_manager.send(event.connection_id, passive_player_view)
            resources.games_table.put_item(Item=serialize(game))

        resources.queue_table.delete_item(Key={"connection-id": queued_connection_id})

    else:
        resources.queue_table.put_item(Item={"connection-id": event.connection_id})
