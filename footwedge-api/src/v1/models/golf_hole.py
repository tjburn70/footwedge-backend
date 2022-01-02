from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GolfHoleBody(BaseModel):
    name: Optional[str] = None
    hole_number: int
    par: int
    distance: int
    unit: str


class GolfHole(GolfHoleBody):
    hole_id: str
    created_ts: datetime
    touched_ts: Optional[datetime] = None
