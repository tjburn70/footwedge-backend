from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    COGNITO_DOMAIN: str = 'footwedge-dev'
    COGNITO_REGION: str = 'us-east-2'
    STREAM_SERVICE_COGNITO_CLIENT_ID: str
    STREAM_SERVICE_COGNITO_CLIENT_SECRET: str
    FOOTWEDGE_API_URL: AnyHttpUrl
    SEARCH_SERVICE_API_URL: AnyHttpUrl


settings = Settings(_env_file='./src/.env', _env_file_encoding='utf-8')
