from pydantic_settings import BaseSettings  # Must use this import
from pydantic import Field

class Settings(BaseSettings):
    database_username: str = Field(..., env="DATABASE_USERNAME")
    database_password: str = Field(..., env="DATABASE_PASSWORD")
    database_hostname: str = Field(..., env="DATABASE_HOSTNAME")
    database_port: str = Field(..., env="DATABASE_PORT")
    database_name: str = Field(..., env="DATABASE_NAME")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()