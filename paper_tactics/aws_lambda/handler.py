import traceback

from paper_tactics.aws_lambda.event import LambdaEvent
from paper_tactics.aws_lambda.resources import LambdaResources


def lambda_handler(handler):
    resources = LambdaResources()

    def decorated_handler(event_dict, context):
        event = LambdaEvent(event_dict)
        resources.event_dict = event_dict

        try:
            handler(event, resources)
        except Exception:
            print("EXCEPTION:", traceback.format_exc())

        return {"statusCode": 200}

    return decorated_handler
