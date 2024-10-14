from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# Esto se sebera de importar en la clases de Models
db = SQLAlchemy()


def create_app(config_filename):
    print("*********Incico APP *********")
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    # Inciacion Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Define el loader para obtener el usuario desde su id
    @login_manager.user_loader
    def load_user(user_id):
        # Debe ser el método que retorna el usuario por id
        return User.get_user_db(user_id)

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

        print("---- ALL blueprint resgistrados")

    return app
