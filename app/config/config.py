import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(dotenv_path=find_dotenv(".env"))


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    UMBLER_TALk_API_KEY: str = os.getenv("UMBLER_TALk_API_KEY", "")
    ORGANIZATION_ID: str = os.getenv("ORGANIZATION_ID", "aBPcN3RyveVG41Pn")

    model_config = SettingsConfigDict(env_file=(".env",), env_file_encoding="utf-8")


settings = Settings()
