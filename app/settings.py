from enum import Enum
from pathlib import Path, PosixPath
from typing import Dict

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

from app.api.authorization.settings import AuthJWT


class LogLevel(str, Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class UserRoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"
    ANY = "any"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    ENDPOINT_PERMISSIONS: Dict[str, list[str]] = {}

    DIRECTORY: PosixPath = Path(__file__).resolve().parent.parent

    PROJECT_TITLE: str
    # FastAPI
    FAST_API_PORT: str
    FAST_API_PREFIX: str

    log_level: LogLevel = LogLevel.INFO

    # POSTGRES
    POSTGRES_HOST: str  # for makefile target dev
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    auth_jwt: AuthJWT = AuthJWT()

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
        )

    model_config = SettingsConfigDict(
        env_file=".env.develop",
        env_file_encoding="utf-8",
    )


settings = Settings()
