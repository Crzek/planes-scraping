from dotenv import dotenv_values
import os
import datetime
import logging

logger = logging.getLogger(__name__)

ENV_FILE = os.getenv("ENV_FILE",)
# Asegúrate de que no se cargue el archivo .env por defecto
env_values = dotenv_values(ENV_FILE, verbose=True)

if env_values:
    logger.info("--- ENV_FILE: %s, type: %s", ENV_FILE, type(ENV_FILE))
    logger.info("--- Cargando: %s", ENV_FILE)
    logger.info(".env Cargadas")

PATH_STATIC = "static/"
PATH_STATIC_DATA = PATH_STATIC + "data/"

TODAY = datetime.date.today()
TOMORROW = datetime.date.today() + datetime.timedelta(days=1)
START_DEL = 7
END_DEL = 3
CARACTER_NOT_FLIGHT = "   "

PAS = env_values.get("password")
USER = env_values.get("user")
URL = env_values.get("base_url")


PATH_BROWSER = env_values.get("PATH_BROWSER", None)
PATH_DRIVER = env_values.get("PATH_CHROMEDRIVER", None)
logger.info("--- PATH_BROWSER: %s", PATH_BROWSER)
logger.info("--- PATH_DRIVER: %s", PATH_DRIVER)

SQLALCHEMY_DATABASE_URL = env_values.get("SQLALCHEMY_DATABASE_URL")
