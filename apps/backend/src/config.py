from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server settings
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000

    # OpenAI settings
    openai_api_key: str
    llm_provider: str = "openai"
    llm_model: str = "gpt-5-nano"
    llm_temperature: float = 0.7

    # Google Search settings
    google_search_api_key: str | None = None
    google_search_engine_id: str | None = None

    # Wextractor settings
    wextractor_api_key: str
    wextractor_api_url: str = "https://api.wextractor.com"

    # App settings
    preply_app_id_google: str = "com.preply.android"
    preply_app_id_apple: str = "1400521332"

    class Config:
        env_file = ".env"

settings = Settings()