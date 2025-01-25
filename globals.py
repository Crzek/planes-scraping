from dotenv import load_dotenv
import os
import datetime

ENV_FILE = os.getenv("ENV_FILE")
load = load_dotenv(ENV_FILE)

if load:
    print("--- Cargando: ", ENV_FILE)
    print(".env Cargadas")


PATH_STATIC = "static/"
PATH_STATIC_DATA = PATH_STATIC + "data/"

TODAY = datetime.date.today()
TOMORROW = datetime.date.today() + datetime.timedelta(days=1)
START_DEL = 7
END_DEL = 3

PAS = os.getenv("password")
USER = os.getenv("user")
URL = os.getenv("base_url")

PATH_BROWSER = os.getenv("PATH_BROWSER", None)
PATH_DRIVER = os.getenv("PATH_CHROMEDRIVER", None)
print("--- PATH_DRIVER", PATH_DRIVER)
print("--- PATH_BROWSER", PATH_BROWSER)

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
