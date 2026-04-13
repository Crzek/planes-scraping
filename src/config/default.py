import os
from src.core.settings import settings


def _build_postgres_uri_from_parts() -> str | None:
    user = settings.DATABASE_USER
    password = settings.DATABASE_PASS
    host = settings.DATABASE_HOST
    port = settings.DATABASE_PORT
    database = settings.DATABASE_NAME

    if not all([user, password, host, port, database]):
        return None

    return settings.DATABASE_URL

class BaseConfig:
    SECRET_KEY = settings.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = (
        _build_postgres_uri_from_parts()
        or settings.DATABASE_URL
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = settings.DEBUG

class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = settings.DEBUG

def get_config_by_name(name: str | None):
    if name == "production-amd" or name == "production":
        return ProductionConfig
    return DevelopmentConfig
