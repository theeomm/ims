from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "IMS"
    debug: bool = False
    database_url: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
