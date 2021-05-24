from enum import Enum
from typing import Any, Optional, List

from pydantic import BaseModel

from .golf_club import GolfClub
from .golf_course import GolfCourse
from .golf_round import GolfRound
from .tee_box import TeeBox
from .user import User


class Status(str, Enum):
    success = "success"
    failure = "failure"
    error = "error"


class FootwedgeApiMetadata(BaseModel):
    uri: Optional[str]


class FootwedgeApiResponse(BaseModel):
    status: Status
    data: Any
    message: Optional[str]
    metadata: Optional[FootwedgeApiMetadata]


class GetGolfClubResponse(FootwedgeApiResponse):
    data: Optional[GolfClub]


class GetGolfCourseResponse(FootwedgeApiResponse):
    data: Optional[GolfCourse]


class GetGolfCoursesResponse(FootwedgeApiResponse):
    data: Optional[List[GolfCourse]] = []


class GetGolfRoundResponse(FootwedgeApiResponse):
    data: Optional[GolfRound]


class GetGolfRoundsResponse(FootwedgeApiResponse):
    data: Optional[List[GolfRound]] = []


class GetTeeBoxResponse(FootwedgeApiResponse):
    data: Optional[TeeBox]


class GetTeeBoxesResponse(FootwedgeApiResponse):
    data: Optional[List[TeeBox]] = []


class GetUserResponse(FootwedgeApiResponse):
    data: Optional[User]


class PostGolfClubResponse(FootwedgeApiResponse):
    data: GolfClub


class PostGolfCourseResponse(FootwedgeApiResponse):
    data: GolfCourse


class PostGolfRoundResponse(FootwedgeApiResponse):
    data: GolfRound


class PostTeeBoxResponse(FootwedgeApiResponse):
    data: TeeBox


class PostUserResponse(FootwedgeApiResponse):
    data: User


class PutGolfRoundStatResponse(FootwedgeApiResponse):
    data: GolfRound
