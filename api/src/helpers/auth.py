import time
from typing import Dict

from fastapi import (
    HTTPException,
    status,
)
from jose import jwk, jwt
from jose.exceptions import JWTError
from jose.utils import base64url_decode

from cognito_config import cognito_config
from settings import settings


def pull_jwk_from_token(id_token: str) -> Dict:
    headers = jwt.get_unverified_headers(id_token)
    unverified_kid = headers['kid']

    target_jwk = {}
    for key in cognito_config.user_pool_jwks:
        if key['kid'] == unverified_kid:
            target_jwk = key
            break
    return target_jwk


def verify_token_signature(id_token: str):
    target_jwk = pull_jwk_from_token(id_token)
    if not target_jwk:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot find token's jwk in cognito pool jwks"
        )

    public_key = jwk.construct(target_jwk, algorithm='RS256')

    delimiter = '.'
    message, encoded_signature = id_token.rsplit(delimiter, 1)

    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    if not public_key.verify(message.encode('utf-8'), decoded_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature verification failed"
        )


def verify_token_expiration(id_token: str):
    claims = jwt.get_unverified_claims(id_token)
    if time.time() > claims['exp']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Expired"
        )


def decode_token(id_token: str, audience: str = settings.COGNITO_WEB_CLIENT_ID) -> Dict:
    public_key = pull_jwk_from_token(id_token)
    if not public_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot find token's jwk in cognito pool jwks"
        )
    try:
        return jwt.decode(
            id_token,
            public_key,
            algorithms='RS256',
            issuer=cognito_config.issuer_url,
            audience=audience,
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Not Verified",
        )
