from pydantic import BaseModel, Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    username: str
    password: str | None = None
    host: str
    port: int = Field(ge=1, le=65535)
    name: str

    @computed_field
    def url(self) -> str:
        return PostgresDsn(
            schema="postgresql+asyncpg",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        ).unicode_string()


class Settings(BaseSettings):
    db: DatabaseSettings

    model_config = SettingsConfigDict(env_nested_delimiter="__", env_ignore_empty=True)


settings = Settings(_env_file=(".env.example", ".env"))
