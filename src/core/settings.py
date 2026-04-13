from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, SecretStr


# de momento solo para mongo
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",  # permite variables no definidas
    )

    # archivo .env alternativo (opcional)
    ENV_FILE: str | None = None

    # flask
    FLASK_APP: str = "main:app"
    FLASK_ENV: str = "production"
    SECRET_KEY: SecretStr = "key"

    # entrypoint blueprint
    CONFIG_ENV: str = "production"
    DEBUG: bool = False

    @computed_field
    @property
    def PROD(self) -> bool:
        return not self.DEBUG

    # chrome
    PATH_BROWSER: str = "/usr/bin/google-chrome"
    PATH_DRIVER: str = "/usr/local/bin/chromedriver"

    # dB
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    # postgress
    DATABASE_USER: str = "user"
    DATABASE_PASS: str = "pass"
    DATABASE_HOST: str = "host"
    DATABASE_PORT: str = "8888"
    DATABASE_NAME: str = "database"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASS}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.DATABASE_URL

    # escrapy
    user: str = "user"
    password: SecretStr = "pass"
    base_url: str = "https://acbs.private-radar.com/"

    # paths estáticos
    PATH_STATIC: str = "static/"
    PATH_STATIC_DATA: str = "static/data/"
    PATH_STATIC_PDF: str = "static/pdf/"

    # constantes de scraping
    START_DEL: int = 8
    END_DEL: int = 3
    CARACTER_NOT_FLIGHT: str = "   "


settings = Settings()

def print_settings():
    print(Settings())
