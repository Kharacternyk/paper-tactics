import json

from paper_tactics.adapters.aws_api_gateway_player_notifier import (
    AwsApiGatewayPlayerNotifier,
)
from paper_tactics.adapters.dynamodb_game_repository import DynamodbGameRepository
from paper_tactics.adapters.dynamodb_match_request_queue import (
    DynamodbMatchRequestQueue,
)
from paper_tactics.adapters.stdout_logger import StdoutLogger
from paper_tactics.entities.match_request import MatchRequest
from paper_tactics.use_cases.create_game import create_game

player_queue = DynamodbMatchRequestQueue(
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


class ApiAbuseException(Exception):
    pass


def handler(event, context):
    player_notifier = AwsApiGatewayPlayerNotifier(
        "https://"
        + event["requestContext"]["domainName"]
        + "/"
        + event["requestContext"]["stage"]
    )

    try:
        if len(event["body"]) > 2048:
            raise ApiAbuseException(event["body"])
        request = MatchRequest(
            event["requestContext"]["connectionId"],
            json.loads(event["body"]).get("viewData", {}),
        )
    except KeyError as e:
        logger.log_exception(e)
        return {"statusCode": 400}

    create_game(game_repository, player_queue, player_notifier, logger, request)

    return {"statusCode": 200}
