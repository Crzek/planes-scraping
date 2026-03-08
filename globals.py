from dotenv import dotenv_values
import os
import datetime
import logging

logger = logging.getLogger(__name__)

ENV_FILE = os.getenv("ENV_FILE") or None
logger.info("--- ENV_FILE: %s", ENV_FILE)

if ENV_FILE:
    env_values = dotenv_values(ENV_FILE, verbose=True)
else:
    env_values = {}

# Si no hay archivo o no se cargó nada, usar variables del sistema
if not env_values:
    env_values = dict(os.environ)
    logger.info("--- Usando variables de entorno del sistema")
else:
    # Cargar también en el entorno del sistema (os.environ)
    for key, value in env_values.items():
        if value is not None and key not in os.environ:
            os.environ[key] = value
    logger.info("--- ENV Cargando desde archivo: %s", ENV_FILE)

PROD = env_values.get("DEBUG", "False").lower() == "false"

PATH_STATIC = "static/"
PATH_STATIC_DATA = PATH_STATIC + "data/"
PATH_STATIC_PDF = PATH_STATIC + "pdf/"

TODAY = datetime.date.today()
TOMORROW = datetime.date.today() + datetime.timedelta(days=1)
START_DEL = 8
END_DEL = 3
CARACTER_NOT_FLIGHT = "   "

PAS = env_values.get("password")
USER = env_values.get("user")
URL = env_values.get("base_url")


PATH_BROWSER = env_values.get("PATH_BROWSER", None)
PATH_DRIVER = env_values.get("PATH_DRIVER", None)
logger.info("--- PATH_BROWSER: %s", PATH_BROWSER)
logger.info("--- PATH_DRIVER: %s", PATH_DRIVER)

SQLALCHEMY_DATABASE_URL = env_values.get("SQLALCHEMY_DATABASE_URL")
