# src/__init__.py
import logging
from flask import Flask
from flask_migrate import Migrate
from extencions import login_manager, load_user, db, load_env
from .error import register_error_handlers
from src.core.settings import Settings, print_settings
from sqlalchemy.engine import make_url


def create_app():
    print("*********Incico APP *********")
    print_settings()
    load_env()
    settings_obj = Settings()
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=settings_obj.SECRET_KEY.get_secret_value(),
        SQLALCHEMY_DATABASE_URI=settings_obj.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=settings_obj.SQLALCHEMY_TRACK_MODIFICATIONS,
        DEBUG=settings_obj.DEBUG,
    )

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

    try:
        safe_url = make_url(app.config["SQLALCHEMY_DATABASE_URI"]).render_as_string(
            hide_password=True
        )
    except Exception:
        safe_url = "<invalid SQLALCHEMY_DATABASE_URI>"

    logger.info("DB uri: %s", safe_url)

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

    # intenta conectarse a la base de datos
    with app.app_context():
        try:
            with db.engine.connect():
                logger.info("DB connection: OK")
        except Exception: # No existe la base de datos
            logger.exception("DB connection: FAILED")

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
