from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    middle_initial: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date]
    gender: Optional[str] = None
    role: Optional[str] = None
    created_ts: datetime
    touched_ts: Optional[datetime] = None
