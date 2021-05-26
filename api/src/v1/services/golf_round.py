import uuid
from datetime import datetime
from functools import reduce
from typing import Dict, List

from logger import get_logger
from models.user import CognitoUser
from v1.constants import (
    API_VERSION,
    USER_TAG,
    GOLF_ROUND_TAG,
)
from v1.services.golf_course import GolfCourseService
from v1.repositories.golf_course_repository import golf_course_repo
from v1.repositories.golf_round_repository import GolfRoundRepository
from v1.repositories.utils import validate_response
from v1.models.golf_hole import GolfHole
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

logger = get_logger(__name__)


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
        played_on = golf_round_body.played_on.isoformat() if golf_round_body.played_on else None
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
            'played_on': played_on,
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
        validate_response(response)
        golf_round = GolfRound(**response['Attributes'])
        uri = f"/{API_VERSION}/golf-rounds/{golf_round_id}"
        return PutGolfRoundStatResponse(
            status="success",
            data=golf_round,
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

    @staticmethod
    def calculate_up_and_downs(stats: List[GolfRoundStat], hole_id_to_hole: Dict[str, GolfHole]) -> int:
        up_and_downs = 0
        for stat in stats:
            hole = hole_id_to_hole.get(stat.hole_id)
            if not hole:
                logger.info(f"No hole found with id: {stat.hole_id}")
                continue

            if stat.gross_score == hole.par and stat.putts == 1 and stat.chips == 1:
                up_and_downs += 1
        return up_and_downs

    @staticmethod
    def calculate_sand_saves(stats: List[GolfRoundStat], hole_id_to_hole: Dict[str, GolfHole]) -> int:
        sand_saves = 0
        for stat in stats:
            hole = hole_id_to_hole.get(stat.hole_id)
            if not hole:
                logger.info(f"No hole found with id: {stat.hole_id}")
                continue

            if stat.gross_score == hole.par and stat.putts == 1 and stat.greenside_sand_shots == 1:
                sand_saves += 1
        return sand_saves

    @staticmethod
    def calculate_birdies(stats: List[GolfRoundStat], hole_id_to_hole: Dict[str, GolfHole]) -> int:
        birdies = 0
        for stat in stats:
            hole = hole_id_to_hole.get(stat.hole_id)
            if not hole:
                logger.info(f"No hole found with id: {stat.hole_id}")
                continue

            if stat.gross_score == hole.par - 1:
                birdies += 1
        return birdies

    @staticmethod
    def calculate_pars(stats: List[GolfRoundStat], hole_id_to_hole: Dict[str, GolfHole]) -> int:
        pars = 0
        for stat in stats:
            hole = hole_id_to_hole.get(stat.hole_id)
            if not hole:
                logger.info(f"No hole found with id: {stat.hole_id}")
                continue

            if stat.gross_score == hole.par:
                pars += 1
        return pars

    @staticmethod
    def calculate_bogeys(stats: List[GolfRoundStat], hole_id_to_hole: Dict[str, GolfHole]) -> int:
        bogeys = 0
        for stat in stats:
            hole = hole_id_to_hole.get(stat.hole_id)
            if not hole:
                logger.info(f"No hole found with id: {stat.hole_id}")
                continue

            if stat.gross_score == hole.par + 1:
                bogeys += 1
        return bogeys

    @staticmethod
    def calculate_double_bogeys(stats: List[GolfRoundStat], hole_id_to_hole: Dict[str, GolfHole]) -> int:
        double_bogeys = 0
        for stat in stats:
            hole = hole_id_to_hole.get(stat.hole_id)
            if not hole:
                logger.info(f"No hole found with id: {stat.hole_id}")
                continue

            if stat.gross_score == hole.par + 2:
                double_bogeys += 1
        return double_bogeys

    def aggregate_golf_round_stats(self, golf_round_id: str):
        partition_key = self._tag_key(_key=self.user.username)
        sort_key = f"{GOLF_ROUND_TAG}{golf_round_id}"
        response = self.repo.get(
            partition_key=partition_key,
            sort_key=sort_key,
        )
        item = response.get('Item')
        if item:
            stats = [GolfRoundStat(**stat) for stat in item['stats'] if item.get('stats')]
            if not stats:
                return

            golf_course_service = GolfCourseService(repo=golf_course_repo)
            golf_course_id = item.get('golf_course_id', "")
            tee_box_id = item.get('tee_box_id', "")
            hole_id_to_hole = golf_course_service.map_golf_hole_by_id(
                golf_course_id=golf_course_id,
                tee_box_id=tee_box_id,
            )

            def total():
                return lambda x, y: x+y

            putts = reduce(total(), [stat.putts for stat in stats])
            fairways = reduce(total(), [stat.fairway_hit for stat in stats])
            greens_in_regulation = reduce(total(), [stat.green_in_regulation for stat in stats])
            penalties = reduce(total(), [stat.penalties for stat in stats])
            three_putts = reduce(total(), [1 for stat in stats if stat.putts >= 3])
            up_and_downs = self.calculate_up_and_downs(stats, hole_id_to_hole)
            sand_saves = self.calculate_sand_saves(stats, hole_id_to_hole)
            birdies = self.calculate_birdies(stats, hole_id_to_hole)
            pars = self.calculate_pars(stats, hole_id_to_hole)
            bogeys = self.calculate_bogeys(stats, hole_id_to_hole)
            double_bogeys = self.calculate_double_bogeys(stats, hole_id_to_hole)
            return {
                "putts": putts,
                "fairways": fairways,
                "greens_in_regulation": greens_in_regulation,
                "penalties": penalties,
                "three_putts": three_putts,
                "up_and_downs": up_and_downs,
                "sand_saves": sand_saves,
                "birdies": birdies,
                "pars": pars,
                "bogeys": bogeys,
                "double_bogeys": double_bogeys,
            }
