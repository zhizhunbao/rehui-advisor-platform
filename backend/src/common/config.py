from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    env: str = "development"
    port: int = 8000
    api_prefix: str = "/api"
    debug: bool = False

    # Database Mode: "local" | "supabase" | "" (auto)
    db_mode: str = ""

    # Local PostgreSQL (Docker)
    database_url: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""
    supabase_db_url: str = ""  # Direct PostgreSQL connection

    # JWT
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 10080  # 7 days

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 900  # seconds

    # Logging
    log_level: str = "INFO"
    log_dir: str = "logs"

    # LLM Providers
    gemini_api_key: str = ""
    groq_api_key: str = ""
    cohere_api_key: str = ""
    openrouter_api_key: str = ""

    # GitHub API (for higher rate limits)
    github_token: str = ""

    @property
    def is_production(self) -> bool:
        return self.env == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
