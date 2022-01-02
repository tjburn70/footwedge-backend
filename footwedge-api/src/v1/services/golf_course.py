import uuid
from datetime import datetime
from functools import reduce
from typing import Dict

from v1.constants import (
    API_VERSION,
    GOLF_COURSE_TAG,
    TEE_BOX_TAG,
)
from v1.repositories.golf_course_repository import GolfCourseRepository
from v1.repositories.utils import validate_response
from v1.models.golf_hole import GolfHole
from v1.models.tee_box import (
    TeeBox,
    TeeBoxBody,
)
from v1.models.responses import (
    FootwedgeApiMetadata,
    GetTeeBoxResponse,
    GetTeeBoxesResponse,
    PostTeeBoxResponse,
    Status,
)


class GolfCourseService:
    def __init__(self, repo: GolfCourseRepository):
        self.repo = repo

    @staticmethod
    def _tag_key(_key: str):
        return f"{GOLF_COURSE_TAG}{_key}"

    def add_tee_box(
        self, golf_course_id: str, tee_box_body: TeeBoxBody
    ) -> PostTeeBoxResponse:
        partition_key = self._tag_key(_key=golf_course_id)
        tee_box_id = str(uuid.uuid4())
        sort_key = f"{TEE_BOX_TAG}{tee_box_id}"
        created_ts = datetime.now()
        holes = [
            {
                "hole_id": str(uuid.uuid4()),
                "created_ts": created_ts.isoformat(),
                "touched_ts": None,
                **hole.dict(),
            }
            for hole in tee_box_body.holes
        ]
        item = {
            "pk": partition_key,
            "sk": sort_key,
            "tee_box_id": tee_box_id,
            "created_ts": created_ts.isoformat(),
            "touched_ts": None,
            "holes": holes,
            "par": tee_box_body.par,
            "tee_box_color": tee_box_body.tee_box_color,
            "gender": tee_box_body.gender,
            "distance": tee_box_body.distance,
            "unit": tee_box_body.unit,
            "course_rating": tee_box_body.course_rating,
            "slope": tee_box_body.slope,
        }
        response = self.repo.add(item=item)
        validate_response(response)
        uri = f"/{API_VERSION}/golf-courses/{golf_course_id}/tee-boxes/{tee_box_id}"
        tee_box = TeeBox(**item)
        return PostTeeBoxResponse(
            status="success", data=tee_box, metadata=FootwedgeApiMetadata(uri=uri)
        )

    @staticmethod
    def _map_tee_box(raw_tee_box: dict) -> TeeBox:
        tee_box_info = f"{raw_tee_box['tee_box_color']} ({raw_tee_box['course_rating']} | {raw_tee_box['slope']})"
        holes = raw_tee_box["holes"]
        front_nine_holes = holes[:9] if holes else []
        back_nine_holes = holes[9:] if holes else []
        front_nine_yardage = reduce(
            lambda x, y: x + y, [hole["distance"] for hole in front_nine_holes]
        )
        front_nine_par = reduce(
            lambda x, y: x + y, [hole["par"] for hole in front_nine_holes]
        )
        back_nine_yardage = reduce(
            lambda x, y: x + y, [hole["distance"] for hole in back_nine_holes]
        )
        back_nine_par = reduce(
            lambda x, y: x + y, [hole["par"] for hole in back_nine_holes]
        )
        return TeeBox(
            tee_box_info=tee_box_info,
            front_nine_holes=front_nine_holes,
            front_nine_yardage=front_nine_yardage,
            front_nine_par=front_nine_par,
            back_nine_holes=back_nine_holes,
            back_nine_yardage=back_nine_yardage,
            back_nine_par=back_nine_par,
            **raw_tee_box,
        )

    def get_tee_box(self, golf_course_id: str, tee_box_id: str) -> GetTeeBoxResponse:
        partition_key = self._tag_key(_key=golf_course_id)
        sort_key = f"{TEE_BOX_TAG}{tee_box_id}"
        response = self.repo.get(
            partition_key=partition_key,
            sort_key=sort_key,
        )
        item = response.get("Item")
        if item:
            tee_box = self._map_tee_box(raw_tee_box=item)
            return GetTeeBoxResponse(
                status=Status.success,
                data=tee_box,
            )
        return GetTeeBoxResponse(
            status=Status.success,
            data=None,
            message=f"No tee_box found with {tee_box_id}",
        )

    def get_tee_boxes(self, golf_course_id: str) -> GetTeeBoxesResponse:
        partition_key = self._tag_key(_key=golf_course_id)
        response = self.repo.get_tee_boxes(
            partition_key=partition_key,
        )
        items = response.get("Items")
        if items:
            tee_boxes = [self._map_tee_box(raw_tee_box=item) for item in items]
            return GetTeeBoxesResponse(
                status=Status.success,
                data=tee_boxes,
            )
        return GetTeeBoxesResponse(
            status=Status.success,
            data=[],
            message=f"No tee boxes found with golf_course_id {golf_course_id}",
        )

    def map_golf_hole_by_id(
        self, golf_course_id: str, tee_box_id: str
    ) -> Dict[str, GolfHole]:
        partition_key = self._tag_key(_key=golf_course_id)
        sort_key = f"{TEE_BOX_TAG}{tee_box_id}"
        response = self.repo.get(
            partition_key=partition_key,
            sort_key=sort_key,
        )
        item = response.get("Item")
        if item:
            return {hole["hole_id"]: GolfHole(**hole) for hole in item.get("holes", [])}
