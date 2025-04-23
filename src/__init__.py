# src/__init__.py
import logging
from flask import Flask
from extencions import login_manager, load_user, db
from .error import register_error_handlers
import os

def create_app(config_filename):
    print("*********Incico APP *********")
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    
    # crear directorio de logs
    os.makedirs("logs", exist_ok=True)
    
    # Configurar logging (antes que cualquier otra cosa lo use)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/app.log")]
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

    with app.app_context():
        # importamos modelos primero
        from src.auth.models.users import User
        # otros modelos si ubirann
        db.create_all()

        # my blueprints
        # from app import scrapping_bp
        from .auth import auth_bp

        # app.register_blueprint(scrapping_bp)
        app.register_blueprint(auth_bp)

        logger.info("---- ALL blueprint resgistrados")

        # error handlers
        register_error_handlers(app)

    return app
