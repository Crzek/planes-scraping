# src/auth/routes.py
from globals import PATH_STATIC_DATA, PATH_STATIC
import os
from flask import render_template, request, redirect, url_for, send_file, send_from_directory
import datetime
# blueprint
from . import auth_bp

# nuetras routes
from .models.users import User
from flask_login import (
    login_user,  # para logear
    logout_user,  # para deslogear
    login_required,  # para proteger rutas
    current_user  # para saber el usuario actual
)


@auth_bp.route("/")
def auth():
    """
    paguina principal   

    return : redirect a login
    """
    return redirect(url_for("authBP.login"))


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

        if current_user.is_authenticated:
            return redirect(url_for("authBP.vuelos"))

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
                content_html = (
                    f"<p>User ya registrado: "
                    f"<span class='text-gray-700 font-bold'>{email}</span>"
                    f"</br><a href='{url_for('authBP.login')}'"
                    f"class='text-blue-500' > login </a></p>"
                )
                title = "Usuario ya registrado"
                return render_template("generic_content.html", title=title, content=content_html)
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
    from werkzeug.security import check_password_hash  # nopep8

    print(request.method)
    errors = dict()

    if current_user.is_authenticated:
        return redirect(url_for("authBP.vuelos"))

    if request.method == "POST":
        email = request.form["email"]
        passwd = request.form["password"]

        # usuario en DB
        user = User.query.filter_by(email=email).first()

        # ver si esta su email y ver si la contra es correcta
        if user:
            if check_password_hash(user.password, passwd):
                is_loged = login_user(user, remember=True)  # logear
                print("----login----")
                print(url_for("authBP.vuelos", email=email))
                print(url_for("authBP.vuelos"))
                # return redirect(url_for("authBP.vuelos", email=email)) #/vuelos?email=crzerick6@gmail.com
                # return redirect(url_for("authBP.vuelos")) # /vuelos
                return redirect(url_for("authBP.vuelos"))

            errors["pass"] = "Contraseña incorrecta"
        else:
            errors["email"] = "Usuario no existe"

        return render_template("login.html", errors=errors)

    return render_template("login.html", errors=errors)


@auth_bp.route("/logout")
@login_required
def logout():
    """
    logout

    input :
    return :
    """
    logout_user()
    return redirect(url_for("authBP.login"))


@auth_bp.route("/vuelos/<string:remake>", methods=["POST"])
@auth_bp.route("/vuelos", methods=["GET", "POST"])
@login_required
def vuelos(remake: str = None):
    """
    generacion de vuelos

    remake:str
    values: None, "remake"
    PATH origin: /app/src/auth/templates/static/js/vuelos.js
    """
    # /app/src/auth

    TODAY = datetime.date.today()
    TOMORROW = datetime.date.today() + datetime.timedelta(days=1)
    if request.method == "POST":
        day = request.form['day']
        print("ver Dia", day)
        # generar vuelos
        if day == "today":
            hoy = True
        else:
            hoy = False

        date = TODAY if hoy else TOMORROW

        try:
            filename = f'vuelos-{date}.xlsx'
            getcwd = os.getcwd()
            filepath = (
                f'{getcwd}/{PATH_STATIC_DATA}'
                f'{filename}'  # Ajusta según la ruta real
            )
            print("--filepath---", filepath)

            if not os.path.exists(filepath) or (remake == "remake"):
                from src.app.utils.styles import main_styles
                from src.app.main import main
                # en arm heddin True
                # AMD hideen False
                main(hoy, hidden=True)
                main_styles(hoy)

            return render_template(
                "vuelos.html",
                vuelos=filename,
                day=date,
                today=TODAY, tomorrow=TOMORROW
            )

        except Exception as e:
            print(f"Error {e}")
            return render_template(
                "vuelos.html",
                vuelos=None,
                errors=f"Error al cargar los vuelos::: {e}",
                day=date,
                today=TODAY, tomorrow=TOMORROW

            )

    return render_template("vuelos.html", vuelos=None, today=TODAY, tomorrow=TOMORROW)


@auth_bp.route("/thanks/<string:email>")
def thanks(email: str):
    """
    Paguina de Bienvenida por Registrase

    input : email  para dar la Bienvenida
    return :
    """
    return render_template("thanks.html", email=email)


@auth_bp.route("/descargar/data/<string:filename>", methods=["GET"])
@login_required
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
