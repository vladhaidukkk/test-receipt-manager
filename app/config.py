from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_ignore_empty=True)


settings = Settings(_env_file=(".env.example", ".env"))
