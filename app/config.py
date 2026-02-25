from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PORT: int = Field(default=3000, validation_alias="PORT")
    DATABASE_URL: Optional[str] = Field(default=None, validation_alias="DATABASE_URL")
    DB_PATH: str = Field(default="../job-tracker/jobs.db", validation_alias="DB_PATH")
    UPLOAD_DIR: str = Field(
        default="../job-tracker/uploads", validation_alias="UPLOAD_DIR"
    )

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"sqlite+aiosqlite:///{self.DB_PATH}"


settings = Settings()
