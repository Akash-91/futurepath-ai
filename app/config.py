from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://futurepath:change_me@localhost:5432/futurepath"
    jwt_secret: str = "dev-only-change-me"
    jwt_expire_minutes: int = 30
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    google_client_id: str = ""
    google_client_secret: str = ""
    auth_cookie_name: str = "futurepath_session"
    cookie_secure: bool = False
    resume_storage_path: str = "/app/data/resumes"
    max_resume_size_mb: int = 10
    redis_url: str = "redis://redis:6379/0"
    extractor_version: str = "r1-v1"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
