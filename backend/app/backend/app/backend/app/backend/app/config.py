from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ALFA by Daral Travel"
    DATABASE_URL: str = "sqlite+aiosqlite:///./alfa.db"

    JWT_SECRET_KEY: str = "CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
