# from google.oauth2 import service_account
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


# de momento solo para mongo
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",  # permite variables no definidas
    )

    # flask
    FLASK_APP: str = "main:app"
    FLASK_ENV: str = "production"
    SECRET_KEY: SecretStr = "key"

    # entrypoint blueprint
    CONFIG_ENV: str = "production"
    DEBUG: bool = False

    # chrome
    PATH_BROWSER: str = "/usr/bin/google-chrome"
    PATH_DRIVER: str = "/usr/local/bin/chromedriver"

    # dB path en sqlite
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///midb.db"

    # escrapy
    user: str = "user"
    password: SecretStr = "pass"
    base_url: str = "https://acbs.private-radar.com/"
    
    
settings = Settings()

def print_settings():
    print(settings)
