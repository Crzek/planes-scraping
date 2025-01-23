# dir: auth
from flask import Blueprint

auth_bp = Blueprint(
    "authBP",  # para usar en template html
    __name__,
    template_folder="templates",
    # url_prefix="/auth"
)


from . import routes  # nopep8
