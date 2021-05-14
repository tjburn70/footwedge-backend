from datetime import date
from decimal import Decimal
from pydantic import BaseModel


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
