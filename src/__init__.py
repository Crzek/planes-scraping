# src/__init__.py
import logging
from flask import Flask
from extencions import login_manager, load_user, db, load_env
from flask_migrate import Migrate
from .error import register_error_handlers
import os
from .config.default import get_config_by_name


def create_app():
    print("*********Incico APP *********")
    load_env()
    app = Flask(__name__)
    config_name = os.getenv("FLASK_ENV") or os.getenv("CONFIG_ENV")
    app.config.from_object(get_config_by_name(config_name))

    # # crear directorio de logs
    # os.makedirs("logs", exist_ok=True)

    # Configurar logging (antes que cualquier otra cosa lo use)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d: %(message)s",
        handlers=[
            logging.StreamHandler(),
            # logging.FileHandler("logs/app.log")
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("***** Inicio de la app *****")

    # Inciacion Login Manager
    # login_manager = LoginManager()
    login_manager.init_app(app)

    # en ves de definir la funcion load_user la importamos
    login_manager.user_loader(load_user)
    # redirige a la pagina de login, cuando no esta logeado
    login_manager.login_view = "authBP.login"

    # DDBB
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        # importamos modelos primero para que Alembic los detecte
        from src.auth.models.users import User  # noqa: F401

        # my blueprints
        from .auth import auth_bp
        from .app import scrapping_bp
        from .health import health_bp

        app.register_blueprint(health_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(scrapping_bp)

        logger.info("---- ALL blueprint resgistrados")

        # error handlers
        register_error_handlers(app)

    return app
