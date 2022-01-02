from boto3.dynamodb.conditions import Key

from v1.constants import GOLF_COURSE_TAG
from .base_repository import BaseRepository


class GolfClubRepository(BaseRepository):
    def get_golf_courses(self, partition_key: str):
        return self.table.query(
            KeyConditionExpression=Key("pk").eq(partition_key)
            & Key("sk").begins_with(GOLF_COURSE_TAG)
        )


golf_club_repo = GolfClubRepository()
