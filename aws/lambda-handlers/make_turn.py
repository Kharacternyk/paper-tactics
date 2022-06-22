import json
from typing import Any, cast

from aws_lambda_powertools.tracing import Tracer

from paper_tactics.adapters.aws_api_gateway_player_notifier import (
    AwsApiGatewayPlayerNotifier,
)
from paper_tactics.adapters.dynamodb_game_repository import DynamodbGameRepository
from paper_tactics.adapters.stdout_logger import StdoutLogger
from paper_tactics.entities.cell import Cell
from paper_tactics.use_cases.make_turn import make_turn

game_repository = DynamodbGameRepository(
    "paper-tactics-game-states",
    "id",
    "expiration-time",
    600,
)
logger = StdoutLogger()
tracer = Tracer(service="make-turn")


@tracer.capture_lambda_handler
def handler(event: dict[str, Any], context: Any) -> dict[str, int]:
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
        cell = cast(Cell, tuple(body["cell"]))
        assert len(cell) == 2
    except Exception as e:
        logger.log_exception(e)
        return {"statusCode": 400}

    make_turn(game_repository, player_notifier, logger, game_id, player_id, cell)
    return {"statusCode": 200}
