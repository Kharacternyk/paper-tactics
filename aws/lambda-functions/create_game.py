import json

import boto3

from paper_tactics.game import Game
from paper_tactics.game_io import serialize_to_dynamodb_dict
from paper_tactics.game_view import create_game_view_for_active_player
from paper_tactics.game_view import create_game_view_for_passive_player

dynamodb = boto3.resource("dynamodb")
queue_table = dynamodb.Table("paper-tactics-client-queue")
games_table = dynamodb.Table("paper-tactics-game-states")


def handler(event, context):
    request_context = event["requestContext"]
    request_connection_id = request_context["connectionId"]
    queue_head_connection_id = None

    queue = queue_table.scan(ConsistentRead=True)

    if queue["Count"]:
        queue_head_connection_id = queue["Items"][0]["connection-id"]
        queue_table.delete_item(Key={"connection-id": queue_head_connection_id})
        try_create_game(
            request_context, request_connection_id, queue_head_connection_id
        )
    else:
        add_to_queue(request_connection_id)

    return {"statusCode": 200}


def try_create_game(request_context, request_connection_id, queue_head_connection_id):
    game = Game()
    game.init_players()
    active_player_view = create_game_view_for_active_player(game)
    passive_player_view = create_game_view_for_passive_player(game)

    management_api = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=f"https://{request_context['domainName']}/"
        + request_context["stage"],
    )

    try:
        send_dict(management_api, queue_head_connection_id, active_player_view)
    except management_api.exceptions.GoneException:
        add_to_queue(request_connection_id)
    else:
        send_dict(management_api, request_connection_id, passive_player_view)
        games_table.put_item(Item=serialize_to_dynamodb_dict(game))


def send_dict(management_api, connection_id, data):
    management_api.post_to_connection(
        Data=json.dumps(data, separators=(",", ":")).encode(),
        ConnectionId=connection_id,
    )


def add_to_queue(connection_id):
    queue_table.put_item(Item={"connection-id": connection_id})
