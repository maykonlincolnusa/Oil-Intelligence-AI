from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    api_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_base_prefix: str = "/api"
    api_version: str = "v1"
    auto_create_tables: bool = True

    log_level: str = "INFO"
    log_json: bool = True
    request_id_header: str = "X-Request-ID"

    default_page_limit: int = 100
    max_page_limit: int = 1000

    postgres_db: str = "oil_intelligence"
    postgres_user: str = "oil"
    postgres_password: str = "oil"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    redis_host: str = "localhost"
    redis_port: int = 6379

    celery_market_refresh_minutes: int = 30
    celery_events_refresh_minutes: int = 15
    celery_alerts_refresh_minutes: int = 20

    openai_api_key: str | None = None
    eia_api_key: str | None = None
    fred_api_key: str | None = None
    gdelt_api_key: str | None = None
    sentinel_hub_api_key: str | None = None
    nasa_firms_api_key: str | None = None
    commercial_sat_api_key: str | None = None

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def sync_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def api_version_prefix(self) -> str:
        return f"{self.api_base_prefix}/{self.api_version}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
