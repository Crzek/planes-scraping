from flask import render_template


def register_error_handlers(app):

    @app.errorhandler(404)
    def handle_404(error):
        # return "hola"
        return (render_template("page_404.html", error=error), 404)

    @app.errorhandler(500)
    def handle_500(error):
        return (render_template('page_500.html', error=error), 500)
