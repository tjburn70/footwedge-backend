import uuid
from datetime import datetime

from v1.constants import (
    API_VERSION,
    GOLF_CLUB_TAG,
    GOLF_COURSE_TAG,
)
from v1.repositories.golf_club_repository import GolfClubRepository
from v1.repositories.utils import validate_response
from v1.models.golf_club import (
    GolfClub,
    GolfClubBody,
)
from v1.models.golf_course import (
    GolfCourse,
    GolfCourseBody,
)
from v1.models.responses import (
    FootwedgeApiMetadata,
    GetGolfClubResponse,
    GetGolfCourseResponse,
    GetGolfCoursesResponse,
    PostGolfClubResponse,
    PostGolfCourseResponse,
    Status,
)


class GolfClubService:
    def __init__(self, repo: GolfClubRepository):
        self.repo = repo

    @staticmethod
    def _tag_key(_key: str):
        return f"{GOLF_CLUB_TAG}{_key}"

    def get_golf_club(self, golf_club_id: str) -> GetGolfClubResponse:
        partition_key = self._tag_key(_key=golf_club_id)
        sort_key = partition_key
        response = self.repo.get(
            partition_key=partition_key,
            sort_key=sort_key,
        )
        # TODO: validate response metadata
        item = response.get("Item")
        if item:
            golf_club = GolfClub(**item)
            return GetGolfClubResponse(status=Status.success, data=golf_club)

        return GetGolfClubResponse(
            status=Status.success,
            data=None,
            message=f"No golf club found with id: {golf_club_id}",
        )

    def add_golf_club(self, golf_club_body: GolfClubBody) -> PostGolfClubResponse:
        golf_club_id = golf_club_body.golf_club_id or str(uuid.uuid4())
        golf_club_name = golf_club_body.name
        address = golf_club_body.address
        city = golf_club_body.city
        state_code = golf_club_body.state_code
        county = golf_club_body.county
        zip_code = golf_club_body.zip_code
        phone_number = golf_club_body.phone_number
        email = golf_club_body.email
        website = golf_club_body.website
        partition_key = self._tag_key(_key=golf_club_id)
        sort_key = partition_key
        created_ts = datetime.now()
        item = {
            "pk": partition_key,
            "sk": sort_key,
            "golf_club_id": golf_club_id,
            "name": golf_club_name,
            "address": address,
            "city": city,
            "state_code": state_code,
            "county": county,
            "zip_code": zip_code,
            "phone_number": phone_number,
            "email": email,
            "website": website,
            "created_ts": created_ts.isoformat(),
            "touched_ts": None,
        }
        response = self.repo.add(item=item)
        validate_response(response)
        uri = f"/{API_VERSION}/golf-clubs/{golf_club_id}"
        golf_club = GolfClub(**item)
        return PostGolfClubResponse(
            status=Status.success,
            data=golf_club,
            metadata=FootwedgeApiMetadata(uri=uri),
        )

    def add_golf_course(
        self, golf_club_id: str, golf_course_body: GolfCourseBody
    ) -> PostGolfCourseResponse:
        partition_key = self._tag_key(_key=golf_club_id)
        golf_course_id = str(uuid.uuid4())
        sort_key = f"{GOLF_COURSE_TAG}{golf_course_id}"
        created_ts = datetime.now()
        item = {
            "pk": partition_key,
            "sk": sort_key,
            "golf_club_id": golf_club_id,
            "golf_course_id": golf_course_id,
            "created_ts": created_ts.isoformat(),
            "touched_ts": None,
            **golf_course_body.dict(),
        }
        response = self.repo.add(item=item)
        validate_response(response)
        uri = f"/{API_VERSION}/golf-clubs/{golf_club_id}/golf-courses/{golf_course_id}"
        golf_course = GolfCourse(
            golf_course_id=golf_course_id,
            created_ts=created_ts,
            touched_ts=None,
            **golf_course_body.dict(),
        )
        return PostGolfCourseResponse(
            status=Status.success,
            data=golf_course,
            metadata=FootwedgeApiMetadata(uri=uri),
        )

    def get_golf_courses(
        self,
        golf_club_id: str,
    ) -> GetGolfCoursesResponse:
        partition_key = self._tag_key(_key=golf_club_id)
        response = self.repo.get_golf_courses(partition_key=partition_key)
        items = response.get("Items")
        if items:
            golf_courses = [GolfCourse(**item) for item in items]
            return GetGolfCoursesResponse(
                status=Status.success,
                data=golf_courses,
            )

        return GetGolfCoursesResponse(
            status=Status.success,
            data=[],
            message=f"No golf courses found for found for golf_club_id: {golf_club_id}",
        )

    def get_golf_course(
        self,
        golf_club_id: str,
        golf_course_id: str,
    ) -> GetGolfCourseResponse:
        partition_key = self._tag_key(_key=golf_club_id)
        sort_key = f"{GOLF_COURSE_TAG}{golf_course_id}"
        response = self.repo.get(
            partition_key=partition_key,
            sort_key=sort_key,
        )
        # TODO: validate response metadata
        item = response.get("Item")
        if item:
            golf_course = GolfCourse(**item)
            return GetGolfCourseResponse(
                status=Status.success,
                data=golf_course,
            )

        return GetGolfCourseResponse(
            status=Status.success,
            data=None,
            message=f"No golf course found with id: {golf_course_id} for golf_club_id: {golf_club_id}",
        )
