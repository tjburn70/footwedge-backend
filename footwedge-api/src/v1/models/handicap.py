from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class HandicapBody(BaseModel):
    index: Decimal
    authorized_association: Optional[str] = "USGA"


class Handicap(HandicapBody):
    handicap_id: str
    created_ts: datetime
