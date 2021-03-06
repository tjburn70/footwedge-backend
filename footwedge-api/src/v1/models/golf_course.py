from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GolfCourseBody(BaseModel):
    golf_course_id: Optional[str] = None
    name: str
    num_holes: int


class GolfCourse(GolfCourseBody):
    created_ts: datetime
    touched_ts: Optional[datetime] = None
