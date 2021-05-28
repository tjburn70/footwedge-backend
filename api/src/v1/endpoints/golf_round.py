from fastapi import APIRouter, Depends, Security

from helpers.api_dependencies import get_current_user, authorize_client
from models.user import CognitoUser

from v1.models.golf_round import GolfRoundBody
from v1.models.golf_round_stat import GolfRoundStatBody
from v1.models.responses import (
    GetGolfRoundResponse,
    GetGolfRoundsResponse,
    GetGolfRoundAggregateStats,
    GetGolfRoundsAggregateStats,
    PostGolfRoundResponse,
    PutGolfRoundStatResponse,
)
from v1.repositories.golf_round_repository import golf_round_repo
from v1.services.golf_round import GolfRoundService

READ_SCOPE = 'footwedge-api/golf-rounds.read'
PATH_PREFIX = 'golf-rounds'
router = APIRouter()


@router.get('/', response_model=GetGolfRoundsResponse)
def get_golf_rounds(user: CognitoUser = Depends(get_current_user)):
    service = GolfRoundService(user=user, repo=golf_round_repo)
    return service.get_golf_rounds()


@router.post('/', response_model=PostGolfRoundResponse)
def add_golf_rounds(
        golf_round_body: GolfRoundBody,
        user: CognitoUser = Depends(get_current_user)
):
    service = GolfRoundService(user=user, repo=golf_round_repo)
    return service.add_golf_round(golf_round_body=golf_round_body)


@router.get('/aggregate-stats', response_model=GetGolfRoundsAggregateStats)
def aggregate_all_round_stats(user: CognitoUser = Depends(get_current_user)):
    service = GolfRoundService(user=user, repo=golf_round_repo)
    return service.map_round_id_to_aggregate_stats()


@router.get('/{golf_round_id}', response_model=GetGolfRoundResponse)
def get_golf_round_by_id(
        golf_round_id: str,
        user: CognitoUser = Depends(get_current_user),
):
    service = GolfRoundService(user=user, repo=golf_round_repo)
    return service.get_golf_round(golf_round_id=golf_round_id)


@router.put('/{golf_round_id}/stat', response_model=PutGolfRoundStatResponse)
def add_golf_round_stat(
        golf_round_id: str,
        stat_body: GolfRoundStatBody,
        user: CognitoUser = Depends(get_current_user),
):
    service = GolfRoundService(user=user, repo=golf_round_repo)
    return service.add_golf_round_stat(
        golf_round_id=golf_round_id,
        golf_round_stat_body=stat_body,
    )


@router.get('/{golf_round_id}/aggregate-stats', response_model=GetGolfRoundAggregateStats)
def get_aggregate_round_stats(
        golf_round_id: str,
        user: CognitoUser = Depends(get_current_user),
):
    service = GolfRoundService(user=user, repo=golf_round_repo)
    return service.aggregate_golf_round_stats(
        golf_round_id=golf_round_id,
    )


@router.get('/user/{user_id}', response_model=GetGolfRoundsResponse)
def get_golf_rounds_by_user_id(user_id: str, _: str = Security(authorize_client, scopes=[READ_SCOPE])):
    service = GolfRoundService(repo=golf_round_repo)
    return service.get_golf_rounds_by_user_id(user_id=user_id)

