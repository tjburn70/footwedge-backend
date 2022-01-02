from datetime import datetime
from typing import Optional

from pydantic import BaseModel, AnyHttpUrl


class GolfClubBody(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state_code: Optional[str] = None
    county: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[AnyHttpUrl] = None


class GolfClub(GolfClubBody):
    golf_club_id: str
    created_ts: datetime
    touched_ts: datetime = None
