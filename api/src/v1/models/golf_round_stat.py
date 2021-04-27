from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GolfRoundStatBody(BaseModel):
    hole_id: str
    gross_score: int
    fairway_hit: bool
    green_in_regulation: bool
    putts: int
    chips: int
    greenside_sand_shots: int
    penalties: int


class GolfRoundStat(GolfRoundStatBody):
    golf_round_stat_id: str
    created_ts: datetime
    touched_ts: Optional[datetime] = None
