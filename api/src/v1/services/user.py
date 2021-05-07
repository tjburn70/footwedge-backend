from datetime import datetime

from v1.constants import (
    API_VERSION,
    USER_TAG,
)
from v1.repositories.user_repository import UserRepository
from v1.repositories.utils import validate_response
from v1.models.user import (
    User,
    UserBody,
)

from v1.models.responses import (
    FootwedgeApiMetadata,
    GetUserResponse,
    PostUserResponse,
    Status,
)


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    @staticmethod
    def _tag_key(_key: str):
        return f"{USER_TAG}{_key}"

    def get_user(self, user_id: str) -> GetUserResponse:
        partition_key = self._tag_key(_key=user_id)
        sort_key = partition_key
        response = self.repo.get(
            partition_key=partition_key,
            sort_key=sort_key,
        )
        # TODO: validate response metadata
        item = response.get('Item')
        if item:
            user = User(**item)
            return GetUserResponse(
                status=Status.success,
                data=user
            )

        return GetUserResponse(
            status=Status.success,
            data=None,
            message=f"No golf club found with id: {user_id}"
        )

    def add_user(self, user_body: UserBody) -> PostUserResponse:
        partition_key = self._tag_key(_key=user_body.user_id)
        sort_key = partition_key
        created_ts = datetime.now()
        item = {
            "pk": partition_key,
            "sk": sort_key,
            "created_ts": created_ts.isoformat(),
            "touched_ts": None,
            **user_body.dict()
        }
        response = self.repo.add(item=item)
        validate_response(response)
        uri = f"/{API_VERSION}/users/me"
        user = User(
            created_ts=created_ts,
            touched_ts=None,
            **user_body.dict()
        )
        return PostUserResponse(
            status=Status.success,
            data=user,
            metadata=FootwedgeApiMetadata(uri=uri)
        )
