from fastapi import APIRouter

from v1.models.tee_box import (
    TeeBoxBody,
)
from v1.models.responses import (
    GetTeeBoxResponse,
    GetTeeBoxesResponse,
    PostTeeBoxResponse,
)
from v1.repositories.golf_course_repository import golf_course_repo
from v1.services.golf_course import GolfCourseService

PATH_PREFIX = 'golf-courses'
router = APIRouter()


@router.post('/{golf_course_id}/tee-boxes', response_model=PostTeeBoxResponse)
def add_tee_box(golf_course_id: str, tee_box: TeeBoxBody):
    service = GolfCourseService(repo=golf_course_repo)
    return service.add_tee_box(
        golf_course_id=golf_course_id,
        tee_box_body=tee_box
    )


@router.get('/{golf_course_id}/tee-boxes', response_model=GetTeeBoxesResponse)
def get_tee_boxes(golf_course_id: str):
    service = GolfCourseService(repo=golf_course_repo)
    return service.get_tee_boxes(
        golf_course_id=golf_course_id,
    )


@router.get('/{golf_course_id}/tee-boxes/{tee_box_id}', response_model=GetTeeBoxResponse)
def get_tee_box(golf_course_id: str, tee_box_id: str):
    service = GolfCourseService(repo=golf_course_repo)
    return service.get_tee_box(
        golf_course_id=golf_course_id,
        tee_box_id=tee_box_id,
    )
