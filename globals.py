from dotenv import load_dotenv
import os
import datetime

load = load_dotenv('.env')
if load:
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

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")


PATH_CHROME = os.getenv("PATH_CHROME", None)
PATH_DRIVER = os.getenv("PATH_CHROMEDRIVER", None)
PATH_CHROMIUM = os.getenv("PATH_CHROMIUM", None)
