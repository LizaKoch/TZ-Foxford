from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'foxford api docs'
    description: str = 'API for foxford task'
    database_url: str = 'postgresql+asyncpg://postgres:postgres@localhost/postgres'
    secret: str = 'foxford'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    bot_token: Optional[str] = None
    api_message: Optional[str] = None
    api_client: Optional[str] = None
    con_rabbit: Optional[str] = None

    class Config:
        """Settings config."""

        env_file = '.env'


settings = Settings()
