import json
from decimal import Decimal
from typing import Dict, List, Optional

import aiohttp
from async_property import async_property

from logger import get_logger
from settings import settings
from footwedge_models import GolfRound, TeeBox

logger = get_logger(name=__name__)


class FootwedgeApiClient:

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self._auth_headers = {}

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        await self.session.close()

    @async_property
    async def auth_headers(self) -> Dict[str, str]:
        if not self._auth_headers:
            access_token = await self.get_access_token()
            self._auth_headers['Authorization'] = access_token
        return self._auth_headers

    async def get_access_token(self):
        cognito_token_url = (
            f"https://{settings.COGNTIO_DOMAIN}.auth.{settings.COGNITO_REGION}.amazoncognito.com/oauth2/token"
        )
        payload = {
            'grant_type': 'client_credentials',
            'client_id': settings.STREAM_SERVICE_COGNITO_CLIENT_ID,
            'client_secret': settings.STREAM_SERVICE_COGNITO_CLIENT_SECRET,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        async with self.session.post(url=cognito_token_url, data=payload, headers=headers) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data['access_token']

    async def call_async(self, method: str, path: str, **kwargs) -> Dict:
        url = f"{settings.FOOTWEDGE_API_URL}/{path}"
        logger.info(f"async requesting: {method} {url}")
        kwarg_headers = kwargs.pop('headers', {})
        headers = {**self.auth_headers, **kwarg_headers}
        async with self.session.request(
            method,
            url,
            headers=headers,
            **kwargs
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            logger.info(f"response body: {data}")
            return data

    async def get_golf_rounds(self, user_id: str) -> List[GolfRound]:
        path = f"/golf-rounds/user/{user_id}"
        resp_body = await self.call_async(
            method="get",
            path=path,
        )
        results = resp_body.get('data', [])
        return [GolfRound(**result) for result in results]

    async def get_tee_box(self, golf_course_id: str, tee_box_id: str) -> TeeBox:
        path = f"/golf-courses/{golf_course_id}/tee-boxes/{tee_box_id}"
        resp_body = await self.call_async(
            method="get",
            path=path,
        )
        data = resp_body.get('data')
        if not data:
            message = f"No TeeBox found with id: {tee_box_id}"
            logger.error(message)
            raise Exception(message)
        return TeeBox(**data)

    async def post_handicap(self, user_id: str, handicap_index: Decimal):
        path = f"/handicaps/{user_id}"
        data = {"index": handicap_index, "authorized_association": "USGA"}
        return await self.call_async(
            method="post",
            path=path,
            json=json.loads(json.dumps(data, default=str)),
        )
