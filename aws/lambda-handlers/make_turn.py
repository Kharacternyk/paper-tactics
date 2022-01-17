import json

from paper_tactics.adapters.aws_api_gateway_player_notifier import (
    AwsApiGatewayPlayerNotifier,
)
from paper_tactics.adapters.dynamodb_game_repository import DynamodbGameRepository
from paper_tactics.adapters.stdout_logger import StdoutLogger
from paper_tactics.use_cases.make_turn import make_turn

game_repository = DynamodbGameRepository(
    "paper-tactics-game-states",
    "id",
    "expiration-time",
    600,
)
logger = StdoutLogger()


def handler(event, context):
    player_notifier = AwsApiGatewayPlayerNotifier(
        "https://"
        + event["requestContext"]["domainName"]
        + "/"
        + event["requestContext"]["stage"]
    )

    try:
        player_id = event["requestContext"]["connectionId"]
        body = json.loads(event["body"])
        game_id = body["gameId"]
        cell = tuple(body["cell"])
        assert len(cell) == 2
    except Exception as e:
        logger.log_exception(e)
        return {"statusCode": 400}

    make_turn(game_repository, player_notifier, logger, game_id, player_id, cell)
    return {"statusCode": 200}
