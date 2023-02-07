import os

import boto3
from hypothesis.strategies import composite, integers, text

from paper_tactics.adapters.dynamodb_game_repository import DynamodbGameRepository
from paper_tactics.adapters.dynamodb_match_request_queue import (
    DynamodbMatchRequestQueue,
)


@composite
def dynamodb_match_request_queues(draw) -> DynamodbMatchRequestQueue:
    return DynamodbMatchRequestQueue(*draw(_dynamodb_tables()))


@composite
def dynamodb_game_repositories(draw) -> DynamodbGameRepository:
    return DynamodbGameRepository(*draw(_dynamodb_tables()))


@composite
def _dynamodb_tables(draw):
    table_name = draw(text(min_size=3))
    key = draw(text(min_size=1))
    ttl_key = draw(text(min_size=1))
    ttl_in_seconds = draw(integers(min_value=0, max_value=10**10))

    if key == ttl_key:
        ttl_key = "_" + key

    os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"

    client = boto3.client("dynamodb")

    try:
        client.delete_table(TableName=table_name)
    except client.exceptions.ResourceNotFoundException:
        pass

    client.create_table(
        TableName=table_name,
        KeySchema=[
            {
                "AttributeName": key,
                "KeyType": "HASH",
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": key,
                "AttributeType": "S",
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    return table_name, key, ttl_key, ttl_in_seconds
