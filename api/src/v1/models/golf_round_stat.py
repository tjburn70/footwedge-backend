from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GolfRoundStatBody(BaseModel):
    hole_id: str
    gross_score: int
    fairway_hit: bool
    green_in_regulation: bool
    putts: int
    chips: Optional[int] = None
    greenside_sand_shots: Optional[int] = None
    penalties: Optional[int] = None


class GolfRoundStat(GolfRoundStatBody):
    golf_round_stat_id: str
    created_ts: datetime
    touched_ts: Optional[datetime] = None


class GolfRoundAggregateStats(BaseModel):
    putts: int
    fairways: int
    greens_in_regulation: int
    penalties: Optional[int] = 0
    three_putts: Optional[int] = 0
    up_and_downs: Optional[int] = 0
    sand_saves: Optional[int] = 0
    birdies: Optional[int] = 0
    pars: Optional[int] = 0
    bogeys: Optional[int] = 0
    double_bogeys: Optional[int] = 0
