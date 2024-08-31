from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LINE_CHANNEL_SECRET: str = ''
    LINE_CHANNEL_ACCESS_TOKEN: str = ''
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
