# dir: src/auth
from flask import Blueprint

auth_bp = Blueprint(
    "authBP",  # para usar en template html
    __name__,
    template_folder="templates",
    static_folder="statics",
    static_url_path="/auth/static",
)

from . import routes  # nopep8
