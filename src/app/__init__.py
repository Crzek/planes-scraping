
# dir: app
from flask import Blueprint
import logging


scrapping_bp = Blueprint(
    "scrapBP",
    __name__,
    template_folder="templates",
    url_prefix="/scrapy"
)

logger = logging.getLogger(__name__)

from .routes import routes  # nopep8
