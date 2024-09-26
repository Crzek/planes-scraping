
# dir: app
from flask import Blueprint

scrapping_bp = Blueprint(
    "scrapBP",
    __name__,
    template_folder="templates",
    url_prefix="/scrapy"
)

# si tubieramos rutas la iportariasmos
