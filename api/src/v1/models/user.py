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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class User(UserBody):
    created_ts: datetime
    touched_ts: Optional[datetime] = None
