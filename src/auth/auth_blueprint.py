from flask import Blueprint

auth_bp = Blueprint(
    "authBP",
    __name__,
    template_folder="templates",
    url_prefix="/auth")
