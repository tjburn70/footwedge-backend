import uuid
from datetime import datetime

from boto3.dynamodb.conditions import Key

from v1.constants import GOLF_ROUND_TAG
from v1.models.golf_round_stat import GolfRoundStatBody
from .base_repository import BaseRepository


class GolfRoundRepository(BaseRepository):
    def get_golf_rounds(self, partition_key: str):
        return self.table.query(
            KeyConditionExpression=Key("pk").eq(partition_key)
            & Key("sk").begins_with(GOLF_ROUND_TAG)
        )

    def add_stat(self, partition_key: str, sort_key: str, stat: GolfRoundStatBody):
        key = {"pk": partition_key, "sk": sort_key}
        update_expression = "SET stats = list_append(stats, :i)"
        created_ts = datetime.now()
        item = {
            "golf_round_stat_id": str(uuid.uuid4()),
            "created_ts": created_ts.isoformat(),
            "touched_ts": None,
            **stat.dict(),
        }
        expression_attribute_values = {":i": [item]}
        return self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        )


golf_round_repo = GolfRoundRepository()
