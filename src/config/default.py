import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True

class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False

def get_config_by_name(name: str | None):
    if name == "production-amd" or name == "production":
        return ProductionConfig
    return DevelopmentConfig
