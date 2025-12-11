from pydantic import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "ALFA by Daral Travel"
    APP_ENV: str = "development"

    # Security
    JWT_SECRET: str = "CHANGE_ME_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"

    # Database (PostgreSQL مثال)
    DATABASE_URL: str = "sqlite+aiosqlite:///./alfa.db"

    class Config:
        env_file = ".env"


settings = Settings()
