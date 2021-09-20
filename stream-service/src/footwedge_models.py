from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel


class GolfCourse(BaseModel):
    golf_course_id: str
    golf_course_name: str
    num_holes: int


class GolfClub(BaseModel):
    golf_club_id: str
    golf_club_name: str
    created_ts: str
    touched_ts: str = None
    golf_courses: List[GolfCourse] = []


class GolfRound(BaseModel):
    golf_round_id: str
    golf_course_id: str
    tee_box_id: str
    gross_score: int
    towards_handicap: bool
    played_on: date


class TeeBox(BaseModel):
    tee_box_id: str
    tee_box_color: str
    par: int
    distance: int
    unit: str
    course_rating: Decimal
    slope: int


class User(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: str
    birthdate: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    created_ts: datetime

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
