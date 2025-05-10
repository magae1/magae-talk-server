from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    turn_credential_domain: str = ""
    turn_credential_api_key: str = ""
    env: str = "dev"

    model_config = SettingsConfigDict(env_file=DOTENV_PATH / ".env")


@lru_cache
def get_settings():
    return Settings()
