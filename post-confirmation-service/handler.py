import json
import os
import logging

import requests

FOOTWEDGE_API_URL = os.getenv("FOOTWEDGE_API_URL")
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


def post_user(user_body: dict):
    url = f"{FOOTWEDGE_API_URL}/users"
    resp = requests.post(
        url=url,
        json=user_body,
    )
    if not resp.ok:
        logger.error(msg=f"Failed to create user, due to: {resp.text}")
        return

    user_email = user_body['email']
    logger.info(f"Successfully created user with email: {user_email}")


def create_user(event: dict) -> dict:
    user_attributes = event["request"]["userAttributes"]
    post_user(user_body=user_attributes)
    return event


def lambda_handler(event, context):
    print(json.dumps(event))
    return create_user(event)
