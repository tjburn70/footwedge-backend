from typing import List

from database import SingletonDynamodbClient

DYNAMO_TABLE_NAME = 'FootwedgeTable'


class BaseRepository:

    def __init__(self):
        self.db_resource = SingletonDynamodbClient.get_dynamo_resource()
        self.table = self.db_resource.Table(DYNAMO_TABLE_NAME)

    def get(
            self,
            partition_key: str,
            sort_key: str,
    ) -> dict:
        primary_key = {
            'pk': partition_key,
            'sk': sort_key
        }
        return self.table.get_item(
            Key=primary_key
        )

    def get_attributes(
            self,
            partition_key: str,
            sort_key: str,
            attributes: List[str],
    ) -> dict:
        primary_key = {
            'pk': partition_key,
            'sk': sort_key
        }
        projection_expression = ', '.join(attributes)
        return self.table.get_item(
            Key=primary_key,
            ProjectionExpression=projection_expression,
        )

    def add(self, item: dict) -> dict:
        return self.table.put_item(
            Item=item,
        )
