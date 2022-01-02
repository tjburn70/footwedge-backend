from typing import Optional

import boto3
from boto3_type_annotations.dynamodb import Client
from boto3_type_annotations.dynamodb import ServiceResource

from settings import settings


class SingletonDynamodbClient:
    dynamodb_client: Optional[Client] = None
    dynamodb_resource: Optional[ServiceResource] = None

    @classmethod
    def get_dynamo_client(cls) -> Client:
        if cls.dynamodb_client is None:
            cls.dynamodb_client = boto3.client(
                "dynamodb", endpoint_url=settings.DYNAMO_DB_URL
            )

        return cls.dynamodb_client

    @classmethod
    def get_dynamo_resource(cls) -> ServiceResource:
        if cls.dynamodb_resource is None:
            cls.dynamodb_resource = boto3.resource(
                "dynamodb", endpoint_url=settings.DYNAMO_DB_URL
            )

        return cls.dynamodb_resource
