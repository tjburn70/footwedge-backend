from boto3.dynamodb.conditions import Key

from v1.constants import TEE_BOX_TAG
from .base_repository import BaseRepository


class GolfCourseRepository(BaseRepository):

    def get_tee_boxes(self, partition_key: str):
        return self.table.query(
            KeyConditionExpression=Key('pk').eq(partition_key) & Key('sk').begins_with(TEE_BOX_TAG)
        )


golf_course_repo = GolfCourseRepository()
