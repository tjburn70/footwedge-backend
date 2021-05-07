from fastapi import (
    Depends,
    Header,
    HTTPException,
    status,
)

from helpers import auth
from models.user import User
from settings import settings


def get_token(authorization: str = Header(...)):
    delimiter = ' '
    auth_pieces = authorization.split(delimiter)
    if len(auth_pieces) != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Authorization Header'
        )


def get_current_user(id_token: str = Depends(get_token)):
    auth.verify_token_signature(id_token)
    auth.verify_token_expiration(id_token)
    cognito_user_info = auth.decode_token(
        id_token=id_token,
        audience=settings.COGNITO_WEB_CLIENT_ID,
    )
    return User(cognito_user_info=cognito_user_info)
