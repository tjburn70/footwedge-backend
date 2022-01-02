import json

from mangum import Mangum

from main import app

handler = Mangum(app)


def lambda_handler(event, context):
    print(json.dumps(event))

    resp = handler(event, context)
    print(f"lambda response: {resp}")
    return resp
