import os
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_env = load_dotenv(".env")

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):  # user_id es un string 3
    from src.auth.models.users import User  # nopep8
    # metodos staticos de la clase User
    print("load_user", user_id, type(user_id))
    user = User.get_user_db(user_id=user_id)
    return user


def get_file() -> str:
    name = os.getenv("CONFIG_ENV")
    print("***getenv**", name, type(name))
    if (name == "development"):
        f = "config/dev.py"
    else:  # (name == "production")
        f = "config/prod.py"

    print("***file_conf***", f)
    return f
