from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # ==================== SERVER CONFIGURATION ====================
    APP_NAME: str = Field(default="RapidAPI Auto Parts Dumper", description="Application name")
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    ENVIRONMENT: str = Field(default="development", description="Environment")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    # ==================== CORS CONFIGURATION ====================
    FRONTEND_URL: str = Field(default="http://localhost:3000", description="Frontend URL")

    # ==================== RAPIDAPI CONFIGURATION (4 keys) ====================
    RAPIDAPI_KEY_1: str = Field(default="", description="RapidAPI key 1")
    RAPIDAPI_KEY_2: str = Field(default="", description="RapidAPI key 2")
    RAPIDAPI_KEY_3: str = Field(default="", description="RapidAPI key 3")
    RAPIDAPI_KEY_4: str = Field(default="", description="RapidAPI key 4")
    RAPIDAPI_HOST: str = Field(default="auto-parts-catalog.p.rapidapi.com", description="RapidAPI host header")
    RAPIDAPI_BASE_URL: str = Field(default="https://auto-parts-catalog.p.rapidapi.com", description="RapidAPI base URL")
    RAPIDAPI_TIMEOUT: float = Field(default=30.0, description="HTTP request timeout (seconds)")

    DEFAULT_LANG_ID: int = Field(default=4, description="Default language ID (4 = English GB)")
    DEFAULT_COUNTRY_FILTER_ID: int = Field(default=63, description="Default country filter ID (63 = Germany)")

    # ==================== DATABASE CONFIGURATION ====================
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    POSTGRES_DB: str = Field(default="autoparts", description="Database name")
    POSTGRES_USER: str = Field(default="autoparts", description="Database user")
    POSTGRES_PASSWORD: str = Field(default="", description="Database password")

    # ==================== DUMP TUNING ====================
    DUMP_DELAY_MS: int = Field(default=100, description="Delay between requests per key (ms)")
    COOLDOWN_429_SEC: int = Field(default=60, description="Cooldown after 429 (per-minute rate limit)")
    COOLDOWN_403_SEC: int = Field(default=3600, description="Cooldown after 403 (likely quota exhausted)")
    COOLDOWN_5XX_SEC: int = Field(default=10, description="Cooldown after 5xx server error")
    KEY_EXHAUSTION_THRESHOLD_SEC: int = Field(
        default=21600,
        description="If all keys are cooling for longer than this (seconds), assume quota exhaustion and pause the job",
    )
    MAX_TRANSIENT_RETRIES: int = Field(default=3, description="Max retries per request on transient errors")

    # ==================== DERIVED PROPERTIES ====================
    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def rapidapi_keys(self) -> list[str]:
        return [
            k
            for k in (
                self.RAPIDAPI_KEY_1,
                self.RAPIDAPI_KEY_2,
                self.RAPIDAPI_KEY_3,
                self.RAPIDAPI_KEY_4,
            )
            if k
        ]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
