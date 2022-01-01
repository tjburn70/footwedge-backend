import uuid
from datetime import datetime

from v1.constants import (
    API_VERSION,
    USER_TAG,
    HANDICAP_TAG,
)
from v1.repositories.handicap_repository import HandicapRepository
from v1.repositories.utils import validate_response
from v1.models.handicap import (
    HandicapBody,
    Handicap,
)
from v1.models.responses import (
    FootwedgeApiMetadata,
    GetActiveHandicapResponse,
    GetHandicapsResponse,
    PostHandicapResponse,
    Status,
)


class HandicapService:

    def __init__(self, repo: HandicapRepository):
        self.repo = repo

    @staticmethod
    def _tag_key(_key: str):
        return f"{USER_TAG}{_key}"

    def add_handicap(
            self,
            handicap_body: HandicapBody,
            user_id: str
    ) -> PostHandicapResponse:
        partition_key = self._tag_key(_key=user_id)
        created_ts = datetime.utcnow().isoformat()
        sort_key = f"{HANDICAP_TAG}{created_ts}"
        handicap_id = str(uuid.uuid4())
        item = {
            'pk': partition_key,
            'sk': sort_key,
            'handicap_id': handicap_id,
            'index': handicap_body.index,
            'authorized_association': handicap_body.authorized_association,
            'created_ts': created_ts,
        }
        response = self.repo.add(item=item)
        validate_response(response)
        uri = f"/{API_VERSION}/handicaps/"
        handicap = Handicap(**item)
        return PostHandicapResponse(
            status="success",
            data=handicap,
            metadata=FootwedgeApiMetadata(uri=uri)
        )

    def get_active_handicap(self, user_id: str) -> GetActiveHandicapResponse:
        partition_key = self._tag_key(_key=user_id)
        response = self.repo.get_user_handicaps(partition_key=partition_key, scan_index_forward=False)
        items = response.get('Items')
        if items:
            active_handicap = Handicap(**items[0])
            return GetActiveHandicapResponse(
                status=Status.success,
                data=active_handicap,
            )
        return GetActiveHandicapResponse(
            status=Status.success,
            data=None,
            message=f"No handicap item found for found for user: {user_id}",
        )

    def get_all_handicaps(self, user_id: str) -> GetHandicapsResponse:
        partition_key = self._tag_key(_key=user_id)
        response = self.repo.get_user_handicaps(partition_key=partition_key, scan_index_forward=False)
        items = response.get('Items')
        if items:
            handicaps = [Handicap(**item) for item in items]
            return GetHandicapsResponse(
                status=Status.success,
                data=handicaps,
            )
        return GetHandicapsResponse(
            status=Status.success,
            data=[],
            message=f"No handicaps found for found for user: {user_id}",
        )
