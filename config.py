from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "11mandoni24"
    DB_NAME: str = "retailOrdering"

    JWT_SECRET_KEY: str = "b4c2fcdbfcfa9264f2c533dbcf61e11b55bb0a10c17b8264129bd43a04713973"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()