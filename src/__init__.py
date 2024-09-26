from flask import Flask


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    # DDBB
    # from yourapplication.model import db
    # db.init_app(app)

    # my blueprints
    # from app import scrapping_bp
    from .auth import auth_bp

    # app.register_blueprint(scrapping_bp)
    app.register_blueprint(auth_bp)

    print("---- ALL blueprint resgistrados")
    return app
