import json
from typing import Dict, Optional

import aiohttp
from pydantic import BaseModel

from logger import get_logger
from settings import settings
from footwedge_models import GolfClub, GolfCourse, User

logger = get_logger(name=__name__)


class FootwedgeSearchClient:

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self._auth_headers = {}

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        await self.session.close()

    @staticmethod
    def serialize_document_payload(_id: str, model: BaseModel) -> str:
        data = {
            "_id": _id,
            "payload": model.dict(),
        }
        return json.dumps(data, default=str)

    async def call_async(self, method: str, path: str, **kwargs) -> Dict:
        url = f"{settings.FOOTWEDGE_SEARCH_URL}/{path}"
        logger.info(f"async requesting: {method} {url}")
        async with self.session.request(
            method,
            url,
            **kwargs
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            logger.info(f"response body: {data}")
            return data

    async def add_user(self, user_id: str, user: User):
        data = self.serialize_document_payload(_id=user_id, model=user)
        return await self.call_async(
            method="post",
            path="user",
            data=data,
        )

    async def add_golf_club(self, golf_club_id: str, golf_club: GolfClub):
        data = self.serialize_document_payload(_id=golf_club_id, model=golf_club)
        return await self.call_async(
            method="post",
            path="golf-club",
            data=data,
        )

    async def add_golf_course(self, golf_club_id: str, golf_course: GolfCourse):
        path = f"golf-club/{golf_club_id}/golf-course"
        return await self.call_async(
            method="patch",
            path=path,
            data=golf_course.json(),
        )
