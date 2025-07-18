# src/auth/routes.py
from globals import PATH_STATIC, PATH_STATIC_DATA

import os
from flask import render_template, request, redirect, url_for, send_file, send_from_directory
import datetime
# blueprint
from . import auth_bp
import logging

# nuetras routes
from .models.users import User
from flask_login import (
    login_user,  # para logear
    logout_user,  # para deslogear
    login_required,  # para proteger rutas
    current_user  # para saber el usuario actual
)

logger = logging.getLogger(__name__)


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
            logger.info(f"metodo-{request.method} Valor email {email}")
            # verificar mail
            user = User.query.filter_by(email=email).first()
            if not user:
                # hasear passwd
                pass_hash = generate_password_hash(passwd)

                # guarda en DB
                new_user = User(email=email, password=pass_hash)
                db.session.add(new_user)
                db.session.commit()
                logger.info("------SAVED in DB----")
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
        logger.error(f"Error {e}")
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
                logger.info("----login----")
                logger.info(f"login {is_loged}")
                logger.info(url_for("authBP.vuelos", email=email))
                logger.info(url_for("authBP.vuelos"))
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
        # si no se marca es None (no existe)
        select_all = True if request.form.get(
            "select_all") == "all" else False

        logger.info("ver Dia %s", day)
        # generar vuelos
        if day == "today":
            hoy = True
        else:
            hoy = False

        date = TODAY if hoy else TOMORROW
        try:
            filename = f'vuelos-{date}.xlsx'  # antes excel
            name = filename.split(".")[0]
            # f_s = f'vuelos-{date}_s.xlsx'  # excel con stylos
            getcwd = os.getcwd()

            filepath = (
                f'{getcwd}/{PATH_STATIC_DATA}'
                f'{filename}'  # Ajusta según la ruta real
            )
            logger.info("--filepath--- %s", filepath)
            # html_output = getcwd + "/" + PATH_STATIC + "html/" + name + ".html"
            # pdf_output = getcwd + "/" + PATH_STATIC + "pdf/" + name + ".pdf"
            pdf_output = f"{name}.pdf"
            html_output = f"{name}.html"
            logger.info("pdf_output ---- %s", pdf_output)
            if not os.path.exists(filepath) or (remake == "remake"):
                from src.app.utils.styles import main_styles
                from src.app.main import main

                # en arm heddin True
                # AMD hideen False
                title_day, html_table = main(
                    hoy, hidden=False, date=date, select_all=select_all)
                logger.info("title_day -- %s", title_day)
                main_styles(hoy, date=date)

            return render_template(
                "vuelos.html",
                vuelos=filename,
                # file_s=f_s,
                pdf_file=pdf_output,
                html_file=html_output,
                day=date,
                title_day=None,
                # title_day=title_day,
                today=TODAY, tomorrow=TOMORROW
            )

        except Exception as e:
            logger.error(f"Error {e}")
            return render_template(
                "vuelos.html",
                vuelos=None,
                errors=f"Error al cargar los vuelos::: {e}",
                day=date,
                title_day=None,
                today=TODAY, tomorrow=TOMORROW

            )

    return render_template("vuelos.html", vuelos=None, today=TODAY, tomorrow=TOMORROW, title_day=None)


@auth_bp.route("/thanks/<string:email>")
def thanks(email: str):
    """
    Paguina de Bienvenida por Registrase

    input : email  para dar la Bienvenida
    return :
    """
    return render_template("thanks.html", email=email)


@auth_bp.route("/descargar/<string:path>/<string:filename>", methods=["GET"])
@login_required
def descargar(filename: str, path: str = "data"):
    try:

        getcwd = os.getcwd()  # ruta actual
        if path == "data":
            filepath = (
                f'{getcwd}/{PATH_STATIC_DATA}'
                f'{filename}'  # Ajusta según la ruta real
            )
        else:
            filepath = (
                f'{getcwd}/{PATH_STATIC}'
                f'{path}/{filename}'  # Ajusta según la ruta real
            )
        logger.info("descargando - %s", filepath)

        if not os.path.exists(filepath):
            logger.info("Archivo no encontrado: %s", filepath)
            return "Archivo no encontrado", 404

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        logger.info("Error al descargar el archivo: %s", e)
        return "Error al descargar el archivo", 404


@auth_bp.route("/time")
def localTime():
    """
    Para ver la hora local
    input : email  para dar la Bienvenida
    return :
    """
    from globals import TODAY, TOMORROW
    # import pytz
    # from datetime import datetime

    today = datetime.date.today()
    hora = datetime.datetime.now()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    body = f"""
        <h1>Hora local</h1>
        <p>Hoy de varible global: {TODAY}</p>
        <p>Mañana de varible global: {TOMORROW}</p>
        <br/>
        <p>Hoy de datetime: {today}</p>
        <p>Mañana de datetime: {tomorrow}</p>
        <p>Hora local: {hora}</p>
    """
    return render_template("generic_content.html", title="Hora local", content=body)


@auth_bp.route("/table/<string:file_name>")
def page_html_table(file_name: str):
    """
    obtiene el html de la tabla de vuelos
    input : 
    title : str
    body : str
    return :
        template base limpio
    """
    try:
        getcwd = os.getcwd()
        file = f"{getcwd}/{PATH_STATIC}/html/{file_name}"

        if os.path.exists(file):
            logger.info("page_html_table, file: %s", file)
            with open(file, "r", encoding="utf-8") as f:
                content_body = f.read()
            return render_template("base_clean.html", title="Hora local", content=content_body)

        else:
            logger.error("File html No found: %s", file)
            return render_template("base_clean.html", title="Error", content=f"Error al cargar el HTML (Not Found): {file}")

    except Exception as e:
        logger.error("Error al cargar el HTML: %s", e)
        return render_template("base_clean.html", title="Error", content=f"Error al cargar el HTML: {e}")
