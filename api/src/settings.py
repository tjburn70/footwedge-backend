from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    COGNITO_REGION: str = 'us-east-2'
    COGNITO_USER_POOL_ID: str
    COGNITO_WEB_CLIENT_ID: str
    DYNAMO_DB_URL: AnyHttpUrl
    FOOTWEDGE_DYNAMO_TABLE: str


settings = Settings(_env_file='./src/.env', _env_file_encoding='utf-8')
