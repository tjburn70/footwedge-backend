from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBody(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: str
    birthdate: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None


class User(UserBody):
    created_ts: datetime
    touched_ts: Optional[datetime] = None
