from globals import PATH_STATIC_DATA, PATH_STATIC, TODAY, TOMORROW
import os
from flask import render_template, request, redirect, url_for, send_file

# blueprint
from . import auth_bp

# nuetras routes
from .models.users import User


@auth_bp.route("/")
def auth():
    """
    coment

    input :
    return :
    """
    return "auth"


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    to register users:
    La idea es que no se registre, ya que es una app privada que me envie
    un correo personalizado para ver si le doy acceso

    input :
    return :
    """
    from src import db  # SQLalchemy
    from werkzeug.security import generate_password_hash
    try:

        if request.method == "POST":
            email = request.form["email"]
            passwd = request.form["password"]
            print(f"metodo-{request.method} Valor email {email}")
            # verificar mail
            user = User.query.filter_by(email=email).first()
            if not user:
                # hasear passwd
                pass_hash = generate_password_hash(passwd)

                # guarda en DB
                new_user = User(email=email, password=pass_hash)
                db.session.add(new_user)
                db.session.commit()
                print("------SAVED in DB----")
                return redirect(url_for("authBP.thanks", email=email))
            else:
                return f"User ya registrado {email}"
        return render_template("register.html")
    except Exception as e:
        print(f"Error {e}")
        return f"Error {e}"


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    reder login page

    input :
    return :
    """
    from werkzeug.security import check_password_hash

    print(request.method)
    if request.method == "POST":
        email = request.form["email"]
        passwd = request.form["password"]
        print(email)
        print(passwd)
        user = User.query.filter_by(email=email).first()
        print(user)

        errors = dict()
        # ver si esta su email y ver si la contra es correcta
        if user:
            if check_password_hash(user.password, passwd):
                return redirect(url_for("authBP.vuelos", email=email))

            errors["pass"] = "Contraseña incorrecta"
        else:
            errors["email"] = "Usuario no existe"

        return render_template("login.html", errors=errors)

    return render_template("login.html", errors=None)


@auth_bp.route("/vuelos/<string:remake>", methods=["GET", "POST"])
@auth_bp.route("/vuelos", methods=["GET", "POST"])
def vuelos(remake: str = None):
    """
    generacion de vuelos

    remake:str
    values: None, "remake"
    """

    from src.app.utils.styles import main_styles
    from src.app.main import main

    if request.method == "POST":
        day = request.form['day']
        print("ver Dia", day)
        # generar vuelos
        if day == "today":
            hoy = True
        else:
            hoy = False

        try:
            filename = f'vuelos-{TODAY if hoy else TOMORROW}.xlsx'
            getcwd = os.getcwd()
            filepath = (
                f'{getcwd}/{PATH_STATIC_DATA}'
                f'{filepath}'  # Ajusta según la ruta real
            )

            if not os.path.exists(filepath) or (remake == "remake"):
                main(hoy)
                main_styles(hoy)

            return render_template(
                "vuelos.html",
                vuelos=filename,)

        except Exception as e:
            print(f"Error {e}")
            return render_template("vuelos.html", vuelos=None, errros="Error al cargar los vuelos")

    return render_template("vuelos.html", vuelos=None)


@auth_bp.route("/thanks/<string:email>")
def thanks(email: str):
    """
    Paguina de Bienvenida por Registrase

    input : email  para dar la Bienvenida
    return :
    """
    return render_template("thanks.html", email=email)


@auth_bp.route("/descargar/data/<string:filename>", methods=["GET"])
def descargar(filename: str):
    try:

        getcwd = os.getcwd()  # ruta actual
        filepath = (
            f'{getcwd}/{PATH_STATIC_DATA}'
            f'{filename}'  # Ajusta según la ruta real
        )
        print("descargando", filepath)

        if not os.path.exists(filepath):
            print(f"Archivo no encontrado: {filepath}")
            return "Archivo no encontrado", 404

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return "Error al descargar el archivo", 404
