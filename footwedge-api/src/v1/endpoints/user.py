from fastapi import APIRouter, Depends

from helpers.api_dependencies import get_current_user
from models.user import CognitoUser
from v1.models.user import (
    UserBody,
)
from v1.models.responses import (
    GetUserResponse,
    PostUserResponse,
)
from v1.repositories.user_repository import user_repo
from v1.services.user import UserService

PATH_PREFIX = "users"
router = APIRouter()


@router.post("/", response_model=PostUserResponse)
def add_user(user_body: UserBody):
    service = UserService(repo=user_repo)
    return service.add_user(user_body)


@router.get("/me", response_model=GetUserResponse)
def get_user(user: CognitoUser = Depends(get_current_user)):
    user_id = user.username
    service = UserService(repo=user_repo)
    return service.get_user(user_id=user_id)
