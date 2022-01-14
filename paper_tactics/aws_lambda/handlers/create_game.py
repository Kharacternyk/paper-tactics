from paper_tactics.aws_lambda.event import LambdaEvent
from paper_tactics.aws_lambda.handler import lambda_handler
from paper_tactics.aws_lambda.resources import LambdaResources
from paper_tactics.game.model import Game
from paper_tactics.game.model import Player
from paper_tactics.game.serialization.dynamodb import serialize
from paper_tactics.game.view import create_game_view


@lambda_handler
def handler(event: LambdaEvent, resources: LambdaResources):
    queue = resources.queue_table.scan(ConsistentRead=True)

    if queue["Count"]:
        queued_connection_id = queue["Items"][0]["connection-id"]
        game = Game(
            active_player=Player(id=queued_connection_id),
            passive_player=Player(id=event.connection_id),
        )
        game.init_players()

        try:
            resources.connection_manager.send(
                queued_connection_id, create_game_view(game, queued_connection_id)
            )
        except resources.connection_manager.GoneException:
            resources.queue_table.put_item(Item={"connection-id": event.connection_id})
        else:
            resources.connection_manager.send(
                event.connection_id, create_game_view(game, event.connection_id)
            )
            resources.games_table.put_item(Item=serialize(game))

        resources.queue_table.delete_item(Key={"connection-id": queued_connection_id})

    else:
        resources.queue_table.put_item(Item={"connection-id": event.connection_id})
