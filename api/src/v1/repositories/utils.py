from http import HTTPStatus

from fastapi import HTTPException


def validate_response(dynamodb_response: dict):
    response_metadata = dynamodb_response['ResponseMetadata']
    status_code = response_metadata.get('HTTPStatusCode')
    if status_code != HTTPStatus.OK:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
