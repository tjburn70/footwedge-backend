from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import (
    List,
    Optional,
)

from pydantic import BaseModel

from .golf_round_stat import GolfRoundStat, GolfRoundStatBody


class RoundType(str, Enum):
    FRONT_NINE = "f9"
    BACK_NINE = "b9"
    EIGHTEEN_HOLES = "18"


class GolfRoundBody(BaseModel):
    golf_club_id: str
    golf_club_name: str
    golf_course_id: str
    golf_course_name: str
    tee_box_id: str
    tee_box_distance: str
    tee_box_color: str
    tee_box_course_rating: Decimal
    tee_box_par: int
    gross_score: int
    towards_handicap: bool = True
    played_on: date
    round_type: Optional[RoundType] = RoundType.EIGHTEEN_HOLES
    stats: List[GolfRoundStatBody] = []


class GolfRound(GolfRoundBody):
    golf_round_id: str
    stats: List[GolfRoundStat] = []
    created_ts: datetime
    touched_ts: Optional[datetime] = None
