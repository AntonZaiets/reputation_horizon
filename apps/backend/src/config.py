"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    port: int = 8000
    host: str = "0.0.0.0"
    environment: str = "development"

    # LLM Configuration
    llm_provider: str = "openai"
    llm_model: str = "gpt-5-nano"
    llm_temperature: float = 0.7

    # API Keys
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()

