from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Handicap(BaseModel):
    handicap_id: str
    index: Decimal
    authorized_association: Optional[str] = None
    record_start_date: datetime
    record_end_date: datetime
