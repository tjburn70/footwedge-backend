from fastapi import APIRouter

from v1.models.golf_club import (
    GolfClubBody,
)
from v1.models.golf_course import (
    GolfCourseBody,
)
from v1.models.responses import (
    GetGolfClubResponse,
    GetGolfCourseResponse,
    GetGolfCoursesResponse,
    PostGolfClubResponse,
    PostGolfCourseResponse,
)
from v1.repositories.golf_club_repository import golf_club_repo
from v1.services.golf_club import GolfClubService

PATH_PREFIX = 'golf-clubs'
router = APIRouter()


@router.get('/{golf_club_id}', response_model=GetGolfClubResponse)
def get_golf_club(golf_club_id: str):
    service = GolfClubService(repo=golf_club_repo)
    return service.get_golf_club(golf_club_id=golf_club_id)


@router.post('/', response_model=PostGolfClubResponse)
def add_golf_club(golf_club: GolfClubBody):
    service = GolfClubService(repo=golf_club_repo)
    return service.add_golf_club(golf_club_body=golf_club)


@router.post('/{golf_club_id}/golf-courses', response_model=PostGolfCourseResponse)
def add_golf_course(golf_club_id: str, golf_course: GolfCourseBody):
    service = GolfClubService(repo=golf_club_repo)
    return service.add_golf_course(
        golf_club_id=golf_club_id,
        golf_course_body=golf_course,
    )


@router.get('/{golf_club_id}/golf-courses', response_model=GetGolfCoursesResponse)
def get_golf_courses(golf_club_id: str):
    service = GolfClubService(repo=golf_club_repo)
    return service.get_golf_courses(
        golf_club_id=golf_club_id,
    )


@router.get('/{golf_club_id}/golf-courses/{golf_course_id}', response_model=GetGolfCourseResponse)
def get_golf_course(golf_club_id: str, golf_course_id: str):
    service = GolfClubService(repo=golf_club_repo)
    return service.get_golf_course(
        golf_club_id=golf_club_id,
        golf_course_id=golf_course_id,
    )
