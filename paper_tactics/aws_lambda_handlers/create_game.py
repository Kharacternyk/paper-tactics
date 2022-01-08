import boto3

dynamodb = boto3.resource("dynamodb")
queue_table = dynamodb.Table("paper-tactics-client-queue")


def handler(event, context):
    connection_id = event["requestContext"]["connectionId"]
    queue_table.put_item(Item={"connection-id": connection_id})
    return {"statusCode": 200}
