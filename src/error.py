from flask import render_template
from flask_login import current_user


def register_error_handlers(app):

    @app.errorhandler(404)
    def handle_404(error):
        # return "hola"

        is_logged = current_user.is_authenticated
        return (render_template("page_404.html", error=error, islogged=is_logged), 404)

    @app.errorhandler(500)
    def handle_500(error):
        return (render_template('page_500.html', error=error), 500)
