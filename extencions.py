import logging
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()

logger = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):  # user_id es un string 3
    from src.auth.models.users import User  # nopep8
    # metodos staticos de la clase User
    logger.info("load_user: %s - id:%s", user_id, type(user_id))
    user = User.get_user_db(user_id=user_id)
    return user


def load_env() -> None:
    load_dotenv(".env")
