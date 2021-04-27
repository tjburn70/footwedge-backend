from datetime import datetime, date
from typing import (
    List,
    Optional,
)

from pydantic import BaseModel

from .golf_round_stat import GolfRoundStat, GolfRoundStatBody


class GolfRoundBody(BaseModel):
    golf_course_id: str
    tee_box_id: str
    gross_score: int
    towards_handicap: bool = True
    played_on: date
    stats: List[GolfRoundStatBody] = []


class GolfRound(GolfRoundBody):
    golf_round_id: str
    stats: List[GolfRoundStat] = []
    created_ts: datetime
    touched_ts: Optional[datetime] = None
