from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: Optional[str] = None
    api_message: Optional[str] = None
    api_client: Optional[str] = None
    con_rabbit: Optional[str] = None

    class Config:
        """Settings config."""

        env_file = 'src/bot/.env'


settings = Settings()
