from paper_tactics.adapters.aws_api_gateway_player_notifier import (
    AwsApiGatewayPlayerNotifier,
)
from paper_tactics.adapters.dynamodb_game_repository import DynamodbGameRepository
from paper_tactics.adapters.dynamodb_player_queue import DynamodbPlayerQueue
from paper_tactics.adapters.stdout_logger import StdoutLogger
from paper_tactics.use_cases.create_game import create_game

player_queue = DynamodbPlayerQueue(
    "paper-tactics-client-queue",
    "connection-id",
    "expiration-time",
    3600,
)
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
    except KeyError as e:
        logger.log_exception(e)
        return {"statusCode": 400}

    create_game(game_repository, player_queue, player_notifier, logger, player_id)

    return {"statusCode": 200}
