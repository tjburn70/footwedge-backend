import uuid
from datetime import datetime

from models.user import CognitoUser
from v1.constants import (
    API_VERSION,
    USER_TAG,
    GOLF_ROUND_TAG,
)
from v1.repositories.golf_round_repository import GolfRoundRepository
from v1.repositories.utils import validate_response
from v1.models.golf_round import (
    GolfRound,
    GolfRoundBody,
    GolfRoundStat,
    GolfRoundStatBody,
)
from v1.models.responses import (
    FootwedgeApiMetadata,
    GetGolfRoundResponse,
    GetGolfRoundsResponse,
    PostGolfRoundResponse,
    PutGolfRoundStatResponse,
    Status,
)


class GolfRoundService:

    def __init__(self, repo: GolfRoundRepository, user: CognitoUser):
        self.repo = repo
        self.user = user

    @staticmethod
    def _tag_key(_key: str):
        return f"{USER_TAG}{_key}"

    def add_golf_round(
            self,
            golf_round_body: GolfRoundBody,
    ) -> PostGolfRoundResponse:
        partition_key = self._tag_key(_key=self.user.username)
        golf_round_id = str(uuid.uuid4())
        sort_key = f"{GOLF_ROUND_TAG}{golf_round_id}"
        created_ts = datetime.now()
        stats = [
            {
                'golf_round_stat_id': str(uuid.uuid4()),
                'created_ts': created_ts.isoformat(),
                'touched_ts': None,
                **stat.dict()
            }
            for stat in golf_round_body.stats
        ]
        item = {
            'pk': partition_key,
            'sk': sort_key,
            'golf_round_id': golf_round_id,
            'created_ts': created_ts.isoformat(),
            'touched_ts': None,
            'stats': stats,
            'golf_course_id': golf_round_body.golf_course_id,
            'tee_box_id': golf_round_body.tee_box_id,
            'gross_score': golf_round_body.gross_score,
            'towards_handicap': golf_round_body.towards_handicap,
            'played_on': golf_round_body.played_on,
        }
        response = self.repo.add(item=item)
        validate_response(response)
        uri = f"/{API_VERSION}/golf-rounds/{golf_round_id}"
        golf_round = GolfRound(**item)
        return PostGolfRoundResponse(
            status="success",
            data=golf_round,
            metadata=FootwedgeApiMetadata(uri=uri)
        )

    def add_golf_round_stat(
            self,
            golf_round_id: str,
            golf_round_stat_body: GolfRoundStatBody
    ) -> PutGolfRoundStatResponse:
        partition_key = self._tag_key(_key=self.user.username)
        sort_key = f"{GOLF_ROUND_TAG}{golf_round_id}"
        response = self.repo.add_stat(
            partition_key=partition_key,
            sort_key=sort_key,
            stat=golf_round_stat_body,
        )
        print(f"response: {response}")
        validate_response(response)
        uri = f"/{API_VERSION}/golf-rounds/{golf_round_id}"
        return PutGolfRoundStatResponse(
            status="success",
            metadata=FootwedgeApiMetadata(uri=uri)
        )

    def get_golf_rounds(self) -> GetGolfRoundsResponse:
        partition_key = self._tag_key(_key=self.user.username)
        response = self.repo.get_golf_rounds(partition_key=partition_key)
        items = response.get('Items')
        if items:
            golf_rounds = [GolfRound(**item) for item in items]
            return GetGolfRoundsResponse(
                status=Status.success,
                data=golf_rounds,
            )
        return GetGolfRoundsResponse(
            status=Status.success,
            data=[],
            message=f"No golf rounds found for user with id: {self.user.username}"
        )

    def get_golf_round(self, golf_round_id: str) -> GetGolfRoundResponse:
        partition_key = self._tag_key(_key=self.user.username)
        sort_key = f"{GOLF_ROUND_TAG}{golf_round_id}"
        response = self.repo.get(
            partition_key=partition_key,
            sort_key=sort_key,
        )
        item = response.get('Item')
        if item:
            return GetGolfRoundResponse(
                status=Status.success,
                data=GolfRound(**item),
            )
        return GetGolfRoundResponse(
            status=Status.success,
            data=None,
            message=f"No golf_round found with {golf_round_id}"
        )
