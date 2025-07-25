from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "IMS"
    debug: bool = False
    database_url: str


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
