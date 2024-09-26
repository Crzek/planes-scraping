from . import auth_bp

# nuetras routes


@auth_bp.route("/")
def auth():
    """
    coment

    input :
    return :
    """
    return "auth"
