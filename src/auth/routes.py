from .auth_blueprint import auth_bp

# nuetras routes


@auth_bp.route("/")
def auth(arg):
    """
    coment

    input :
    return :
    """
    return "auth"
