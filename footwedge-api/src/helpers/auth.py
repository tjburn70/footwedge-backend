import time
from typing import Dict, List, Optional

from fastapi import (
    HTTPException,
    status,
)
from jose import jwk, jwt
from jose.exceptions import JWTError
from jose.utils import base64url_decode

from cognito_config import cognito_config
from settings import settings


def pull_jwk_from_token(id_token: str) -> Optional[Dict]:
    headers = jwt.get_unverified_headers(id_token)
    unverified_kid = headers["kid"]
    return cognito_config.user_pool_jwks.get(unverified_kid)


def verify_token_signature(token: str):
    target_jwk = pull_jwk_from_token(token)
    if not target_jwk:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot find token's jwk in cognito pool jwks",
        )

    public_key = jwk.construct(target_jwk, algorithm="RS256")

    delimiter = "."
    message, encoded_signature = token.rsplit(delimiter, 1)

    decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
    if not public_key.verify(message.encode("utf-8"), decoded_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature verification failed",
        )


def verify_token_expiration(token: str):
    claims = jwt.get_unverified_claims(token)
    if time.time() > claims["exp"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
        )


def verify_token_scopes(access_token: str, required_scopes: List[str]):
    claims = jwt.get_unverified_claims(access_token)
    token_scopes = claims["scope"].split()
    if not all(required_scope in token_scopes for required_scope in required_scopes):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client does not have access to this operation",
        )


def decode_token(id_token: str, audience: str = settings.COGNITO_WEB_CLIENT_ID) -> Dict:
    public_key = pull_jwk_from_token(id_token)
    if not public_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot find token's jwk in cognito pool jwks",
        )
    try:
        return jwt.decode(
            id_token,
            public_key,
            algorithms="RS256",
            issuer=cognito_config.issuer_url,
            audience=audience,
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Not Verified",
        )
