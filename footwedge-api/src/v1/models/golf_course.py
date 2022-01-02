from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GolfCourseBody(BaseModel):
    name: str
    num_holes: int


class GolfCourse(GolfCourseBody):
    golf_course_id: str
    created_ts: datetime
    touched_ts: Optional[datetime] = None
