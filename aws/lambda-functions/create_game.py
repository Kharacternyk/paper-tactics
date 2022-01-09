import boto3

dynamodb = boto3.resource("dynamodb")
queue_table = dynamodb.Table("paper-tactics-client-queue")


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
    management_api = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=f"https://{request_context['domainName']}/"
        + request_context["stage"],
    )
    try:
        management_api.post_to_connection(
            Data=f"Game created with {request_connection_id}".encode(),
            ConnectionId=queue_head_connection_id,
        )
    except management_api.exceptions.GoneException:
        add_to_queue(request_connection_id)
    else:
        management_api.post_to_connection(
            Data=f"Game created with {queue_head_connection_id}".encode(),
            ConnectionId=request_connection_id,
        )


def add_to_queue(connection_id):
    queue_table.put_item(Item={"connection-id": connection_id})
