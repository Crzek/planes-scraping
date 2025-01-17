from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

# Instacia de SQLalchemy, creada en src/__init__.py
# donde se encuentra el createApp()
from src import db


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(128))
    password: str = db.Column(db.String(128))
    firstname: str = db.Column(db.String(250))
    lastname: str = db.Column(db.String(250))

    # para verificar la contraseña del usuario, mejor desde fuera o abajo
    @staticmethod
    def get_user_db(user_id: int = None, user_email: str = None):
        """
        get user by id or Email

        input : `user_id` -> int
                `user_email` -> string
        return : USER searched or False if it is not in DB
        """
        if user_id is not None:
            return User.query.filter_by(id=user_id).first()
        else:
            return User.query.filter_by(email=user_email).first()

            # si usamos una DB como SQLite, postgres, mySQL

    # si usamos un diccionario como DB
    @staticmethod
    def get(user_id):
        user_data = User.users.get(user_id)
        if user_data:
            return User(**user_data)
        return None

    # si usamos un diccionario como DB
    @staticmethod
    def get_by_username(username):
        for user_data in User.users.values():
            if user_data['username'] == username:
                return User(**user_data)
        return None
