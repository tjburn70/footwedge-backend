from .abstract_task import AbstractTask
from api_clients.footwedge_search_client import FootwedgeSearchClient
from config import GOLF_CLUB_TAG, GOLF_COURSE_TAG
from footwedge_models import GolfClub, GolfCourse

INSERT_AND_MODIFY_EVENTS = ["INSERT", "MODIFY"]
DELETE_EVENT = "DELETE"


class SyncGolfClub(AbstractTask):

    def __init__(self, event_name: str, dynamodb_record: dict):
        super(SyncGolfClub, self).__init__(event_name, dynamodb_record)
        self.partition_key = self.keys["pk"]["S"]
        self.sort_key = self.keys["sk"]["S"]
        self.key_delimiter = "#"
        self.pk_tag = self.partition_key.split(self.key_delimiter)[0]
        self.sk_tag = self.sort_key.split(self.key_delimiter)[0]

    def _parse_attribute(self, key: str, data_type: str):
        return self.image[key][data_type] if self.image.get(key) and self.image[key].get(data_type) else None

    def build_golf_club(self, golf_club_id: str) -> GolfClub:
        name = self.image["name"]["S"]
        created_ts = self._parse_attribute(key="created_ts", data_type="S")
        touched_ts = self._parse_attribute(key="touched_ts", data_type="S")
        return GolfClub(
            golf_club_id=golf_club_id,
            golf_club_name=name,
            created_ts=created_ts,
            touched_ts=touched_ts,
        )

    def build_golf_course(self, golf_course_id: str) -> GolfCourse:
        name = self.image["name"]["S"]
        num_holes = self.image["num_holes"]["N"]
        return GolfCourse(
            golf_course_id=golf_course_id,
            golf_course_name=name,
            num_holes=num_holes,
        )

    async def add_golf_club(self, api_client: FootwedgeSearchClient):
        golf_club_id = self.partition_key.split(self.key_delimiter)[1]
        golf_club = self.build_golf_club(golf_club_id=golf_club_id)
        return await api_client.add_golf_club(
            golf_club=golf_club,
        )

    async def add_golf_course(self, api_client: FootwedgeSearchClient):
        golf_club_id = self.partition_key.split(self.key_delimiter)[1]
        golf_course_id = self.sort_key.split(self.key_delimiter)[1]
        golf_course = self.build_golf_course(golf_course_id=golf_course_id)
        return await api_client.add_golf_course(
            golf_club_id=golf_club_id,
            golf_course=golf_course,
        )

    async def process_record(self):
        async with FootwedgeSearchClient() as api_client:
            if self.event_name in INSERT_AND_MODIFY_EVENTS:
                tag = f"{self.pk_tag}{self.sk_tag}"
                if tag == GOLF_CLUB_TAG:
                    return await self.add_golf_club(api_client)
                elif tag == GOLF_COURSE_TAG:
                    return await self.add_golf_course(api_client)
