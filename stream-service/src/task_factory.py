from typing import Optional

from tasks import (
    abstract_task,
    sync_golf_club,
    sync_user,
    calculate_handicap,
)
from config import (
    GOLF_CLUB_TAG,
    GOLF_COURSE_TAG,
    GOLF_ROUND_TAG,
    USER_TAG,
)
from logger import get_logger

KEY_TAGS_TO_TASK_CLASS = {
    GOLF_CLUB_TAG: sync_golf_club.SyncGolfClub,
    GOLF_COURSE_TAG: sync_golf_club.SyncGolfClub,
    GOLF_ROUND_TAG: calculate_handicap.CalculateHandicap,
    USER_TAG: sync_user.SyncUser,
}
logger = get_logger(name=__name__)


def parse_tag(record_keys: dict):
    pk = record_keys["pk"]["S"]
    sk = record_keys["sk"]["S"]
    delimiter = "#"
    pk_tag = pk.split(delimiter)[0]
    sk_tag = sk.split(delimiter)[0]
    return f"{pk_tag}{sk_tag}"


def task_factory(record: dict) -> Optional[abstract_task.AbstractTask]:
    event_name = record["eventName"]
    dynamodb_record = record["dynamodb"]
    record_keys = dynamodb_record["Keys"]
    tag = parse_tag(record_keys=record_keys)
    task_class = KEY_TAGS_TO_TASK_CLASS.get(tag)
    if task_class:
        logger.info(f"The tag: {tag} maps to task class: {task_class}")
        return task_class(
            event_name=event_name,
            dynamodb_record=dynamodb_record,
        )

    logger.warning(f"The tag: {tag} does not map to any class...ignoring record...")
