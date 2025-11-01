from pathlib import Path
from typing import Any
from pydantic import SecretStr
from pydantic_settings import (
        BaseSettings,
        SettingsConfigDict
)



class Settings(BaseSettings):
    app_name: str