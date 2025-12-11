from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ALFA by Daral Travel"
    ENV: str = "dev"

    # DB
    DATABASE_URL: str = "sqlite+aiosqlite:///./alfa.db"

    # SECURITY
    JWT_SECRET_KEY: str = "CHANGE_ME_IN_ENV"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # OpenAI (AI Layer)
    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
