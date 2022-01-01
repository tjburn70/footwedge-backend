from fastapi import APIRouter, Depends, Security

from helpers.api_dependencies import get_current_user, authorize_client
from models.user import CognitoUser
from v1.models.handicap import HandicapBody
from v1.models.responses import GetActiveHandicapResponse, GetHandicapsResponse, PostHandicapResponse
from v1.repositories.handicap_repository import handicap_repo
from v1.services.handicap import HandicapService


PATH_PREFIX = 'handicaps'
WRITE_SCOPE = "footwedge-api/handicap.write"
router = APIRouter()


@router.get('/', response_model=GetHandicapsResponse)
def get_handicaps(user: CognitoUser = Depends(get_current_user)):
    user_id = user.username
    service = HandicapService(repo=handicap_repo)
    return service.get_all_handicaps(user_id=user_id)


@router.get('/active', response_model=GetActiveHandicapResponse)
def get_active_handicap(user: CognitoUser = Depends(get_current_user)):
    user_id = user.username
    service = HandicapService(repo=handicap_repo)
    return service.get_active_handicap(user_id=user_id)


@router.post('/{user_id}', response_model=PostHandicapResponse)
def add_handicap(
        user_id: str,
        handicap_body: HandicapBody,
        _: str = Security(authorize_client, scopes=[WRITE_SCOPE])
):
    service = HandicapService(repo=handicap_repo)
    return service.add_handicap(
        handicap_body=handicap_body,
        user_id=user_id,
    )
