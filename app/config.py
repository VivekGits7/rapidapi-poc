from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # ==================== SERVER CONFIGURATION ====================
    APP_NAME: str = Field(default="RapidAPI POC", description="Application name")
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    ENVIRONMENT: str = Field(default="development", description="Environment")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    # ==================== CORS CONFIGURATION ====================
    FRONTEND_URL: str = Field(default="http://localhost:3000", description="Frontend URL")

    # ==================== RAPIDAPI CONFIGURATION (3 keys) ====================
    RAPIDAPI_KEY_1: str = Field(default="", description="RapidAPI key 1")
    RAPIDAPI_KEY_2: str = Field(default="", description="RapidAPI key 2")
    RAPIDAPI_KEY_3: str = Field(default="", description="RapidAPI key 3")
    RAPIDAPI_KEY_4: str = Field(default="", description="RapidAPI key 4")
    RAPIDAPI_HOST: str = Field(default="auto-parts-catalog.p.rapidapi.com", description="RapidAPI host header")
    RAPIDAPI_BASE_URL: str = Field(default="https://auto-parts-catalog.p.rapidapi.com", description="RapidAPI base URL")
    RAPIDAPI_TIMEOUT: float = Field(default=30.0, description="HTTP timeout in seconds")

    DEFAULT_LANG_ID: int = Field(default=4, description="Default language ID")
    DEFAULT_COUNTRY_ID: int = Field(default=63, description="Default country filter ID")
    DEFAULT_TYPE_ID: int = Field(default=1, description="Default vehicle type ID")

    # ==================== DATABASE CONFIGURATION ====================
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    POSTGRES_DB: str = Field(default="autoparts", description="Database name")
    POSTGRES_USER: str = Field(default="autoparts", description="Database user")
    POSTGRES_PASSWORD: str = Field(default="autoparts123", description="Database password")

    # ==================== DUMP BUDGET ====================
    DUMP_BUDGET: int = Field(default=400, description="Total API calls allowed for the dump")
    DUMP_MAX_MANUFACTURERS: int = Field(default=3, description="Max manufacturers to fetch models for")
    DUMP_MAX_MODELS: int = Field(default=3, description="Max models to fetch vehicles for")
    DUMP_MAX_VEHICLES: int = Field(default=3, description="Max vehicles to fetch categories for")
    DUMP_MAX_ARTICLE_COMBOS: int = Field(default=3, description="Max vehicle+category combos to fetch articles for")
    DUMP_MAX_ARTICLES_DEEP: int = Field(default=3, description="Max articles to fetch deep details for (details, media, OEM, fitment, cross-refs, search)")
    DUMP_DELAY_MS: int = Field(default=100, description="Delay between requests in ms (100ms = 10 req/sec)")

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def rapidapi_keys(self) -> list[str]:
        return [k for k in [self.RAPIDAPI_KEY_1, self.RAPIDAPI_KEY_2, self.RAPIDAPI_KEY_3, self.RAPIDAPI_KEY_4] if k]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
