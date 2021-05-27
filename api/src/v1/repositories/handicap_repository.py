from boto3.dynamodb.conditions import Key

from .base_repository import BaseRepository
from v1.constants import HANDICAP_TAG


class HandicapRepository(BaseRepository):

    def get_user_handicaps(self, partition_key: str, scan_index_forward: bool = False) -> dict:
        """
        Retrieve all handicap items for a user. Default is to order by created_ts desc.
        :param partition_key:
        :param scan_index_forward: False = order range key by desc True = order range key by asc
        :return:
        """
        return self.table.query(
            KeyConditionExpression=Key('pk').eq(partition_key) & Key('sk').begins_with(HANDICAP_TAG),
            ScanIndexForward=scan_index_forward
        )


handicap_repo = HandicapRepository()
