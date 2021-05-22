from decimal import Decimal
from typing import List

from .abstract_task import AbstractTask
from api_clients.footwedge_api_client import FootwedgeApiClient
from exceptions import SampleSizeTooSmall
from logger import get_logger

logger = get_logger(name=__name__)


class CalculateHandicap(AbstractTask):

    def __init__(self, event_name: str, dynamodb_record: dict):
        super(CalculateHandicap, self).__init__(event_name, dynamodb_record)
        self.partition_key = self.keys["pk"]["S"]
        self.user_id = self.partition_key.split("#")[1]

    @staticmethod
    def calculate_differential(gross_score: int, course_rating: Decimal, slope: int) -> Decimal:
        return ((gross_score - course_rating) * 113) / slope

    @staticmethod
    def determine_sample_size(num_rounds: int) -> int:
        if num_rounds < 5:
            error_message = 'sample size is too small, need at least 5 golf rounds recorded to calculate handicap'
            raise SampleSizeTooSmall(error_message)
        if num_rounds <= 10:
            size = 1
        elif num_rounds <= 19:
            size = 5
        else:
            size = 10

        return size

    def determine_lowest_differential(self, differentials: List[Decimal]) -> List[Decimal]:
        sample_size = self.determine_sample_size(num_rounds=len(differentials))
        if sample_size == len(differentials):
            return differentials
        else:
            sorted_differentials = sorted(differentials)
            lowest_differentials = sorted_differentials[:sample_size]
            return lowest_differentials

    def calculate_handicap_index(self, differentials) -> Decimal:
        lowest_differentials = self.determine_lowest_differential(differentials=differentials)
        handicap_index = (sum(lowest_differentials) / len(lowest_differentials)) * Decimal('0.96')
        return round(handicap_index, 1)

    async def process_record(self):
        if self.event_name in ["INSERT", "DELETE"]:
            async with FootwedgeApiClient() as api_client:
                ordered_golf_rounds = await api_client.get_golf_rounds(user_id=self.user_id)
                if not ordered_golf_rounds:
                    logger.warning(f"The user_id: {self.user_id} does not have any golf_round records")
                    return

                if len(ordered_golf_rounds) > 20:
                    golf_rounds = ordered_golf_rounds[:20]
                else:
                    golf_rounds = ordered_golf_rounds

                differentials = []
                for golf_round in golf_rounds:
                    tee_box = await api_client.get_tee_box(
                        golf_course_id=golf_round.golf_course_id,
                        tee_box_id=golf_round.tee_box_id,
                    )
                    differential = self.calculate_differential(
                        gross_score=golf_round.gross_score,
                        course_rating=tee_box.course_rating,
                        slope=tee_box.slope,
                    )
                    differentials.append(differential)

                try:
                    handicap_index = self.calculate_handicap_index(differentials=differentials)
                except SampleSizeTooSmall as exc:
                    logger.exception(exc)
                    return

                await api_client.post_handicap(
                    user_id=self.user_id,
                    handicap_index=handicap_index,
                )
                success_message = (
                    f"Successfully calculated and added a new handicap: {handicap_index} for user: {self.user_id}"
                )
                logger.info(success_message)
