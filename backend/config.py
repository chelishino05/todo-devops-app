import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application settings
    app_name: str = "Todo List API"
    app_version: str = "1.0.0"
    debug_mode: bool = False

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    # Database settings
    database_name: str = "todos.db"
    database_url: Optional[str] = None

    # CORS settings
    cors_origins: list = ["*"]

    # Monitoring settings
    enable_metrics: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a global settings instance
settings = Settings()
