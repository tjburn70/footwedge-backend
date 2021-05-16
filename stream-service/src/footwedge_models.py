from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel


class GolfCourse(BaseModel):
    golf_course_id: str
    name: str
    num_holes: int
    created_ts: datetime
    touched_ts: Optional[datetime] = None


class GolfClub(BaseModel):
    golf_club_id: str
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state_code: Optional[str] = None
    county: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[AnyHttpUrl] = None
    created_ts: datetime
    touched_ts: datetime = None
    golf_courses: List[GolfCourse] = []


class GolfRound(BaseModel):
    golf_round_id: str
    golf_course_id: str
    tee_box_id: str
    user_id: str
    gross_score: int
    towards_handicap: bool
    played_on: date


class TeeBox(BaseModel):
    tee_box_id: str
    golf_course_id: str
    tee_color: str
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
