from datetime import datetime
from decimal import Decimal
from functools import reduce
from typing import Optional, List

from pydantic import BaseModel

from .golf_hole import (
    GolfHole,
    GolfHoleBody,
)


class TeeBoxBody(BaseModel):
    tee_box_color: str
    gender: str
    par: int
    distance: int
    unit: str
    course_rating: Decimal
    slope: int
    holes: List[GolfHoleBody] = []


class TeeBox(TeeBoxBody):
    tee_box_id: str
    holes: List[GolfHole] = []
    tee_box_info: str
    front_nine_holes: List[GolfHole] = []
    back_nine_holes: List[GolfHole] = []
    front_nine_yardage: Optional[int]
    front_nine_par: Optional[int]
    back_nine_yardage: Optional[int]
    back_nine_par: Optional[int]
    created_ts: datetime
    touched_ts: Optional[datetime] = None
