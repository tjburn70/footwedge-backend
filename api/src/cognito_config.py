import requests

from settings import settings


class CognitoConfig:

    def __init__(self, aws_region: str, user_pool_id: str):
        self.aws_region = aws_region
        self.user_pool_id = user_pool_id
        self._user_pool_jwks = None

    @property
    def issuer_url(self):
        return f"https://cognito-idp/{self.aws_region}.amazonaws.com/{self.user_pool_id}"

    @property
    def user_pool_jwks(self):
        if self._user_pool_jwks is None:
            self._user_pool_jwks = self._fetch_user_pool_jwks()
        return self._user_pool_jwks

    def _fetch_user_pool_jwks(self):
        url = f'{self.issuer_url}/.well_known/jwks.json'
        resp = requests.get(url)
        resp_body = resp.json()
        keys = resp_body.get('keys', [])
        return {key['kid']: key for key in keys}


cognito_config = CognitoConfig(
    aws_region=settings.COGNITO_REGION,
    user_pool_id=settings.COGNITO_USER_POOL_ID,
)
