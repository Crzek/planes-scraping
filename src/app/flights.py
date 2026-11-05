"""Obtencion de vuelos: API de private-radar primero, Playwright como respaldo."""
import asyncio
import datetime
import logging

from src.app.api.adapter import parse_bookings
from src.app.api.client import PrivateRadarClient
from src.app.api.errors import ApiError
from src.app.automation.main_scraper import main_scraper
from src.app.models.aircraft import AirCraft
from src.app.utils import utils
from src.app.utils.utils import clas_to_series, save_book
from src.core.settings import settings as default_settings

logger = logging.getLogger(__name__)


class FlightsUnavailable(Exception):
    """Ninguna fuente pudo producir los vuelos solicitados."""


def reset_state() -> None:
    """Vacia las reservas acumuladas para no mezclar intentos distintos."""
    AirCraft.all_reservas = {}
    utils.BOOKS.clear()


def _from_api(today: bool, day: datetime.date, cfg):
    client = PrivateRadarClient(
        email=cfg.user,
        password=cfg.password.get_secret_value(),
        login_url=cfg.API_LOGIN_URL,
        bookings_url=cfg.API_BOOKINGS_URL,
        timeout=cfg.API_TIMEOUT,
        extra_ca_file=cfg.API_EXTRA_CA_FILE,
    )
    bookings = parse_bookings(client.get_bookings(day))
    for b in bookings:
        save_book(b.takeoff, b.landing, b.person, b.registration)
    *_, html_table = clas_to_series(today=today, date=day)
    return None, html_table


def get_flights(
    today: bool = False,
    hidden: bool = True,
    date: datetime.date | None = None,
    select_all: bool = False,
    cfg=None,
):
    """Devuelve ``(title_day, html_table)`` igual que ``main_scraper``.

    Con ``USE_API_FIRST`` activo intenta la API y, ante cualquier fallo,
    descarta lo acumulado y ejecuta Playwright.
    """
    cfg = cfg or default_settings
    day = date or (datetime.date.today()
                   + datetime.timedelta(days=0 if today else 1))
    api_attempted = False

    if cfg.USE_API_FIRST:
        api_attempted = True
        reset_state()
        try:
            result = _from_api(today, day, cfg)
            logger.info("fuente de vuelos: api")
            return result
        except ApiError as e:
            logger.warning(
                "fuente de vuelos: api fallo (%s); fallback a playwright",
                e.reason)
        except Exception as e:  # noqa: BLE001 - cualquier fallo activa el fallback
            logger.warning(
                "fuente de vuelos: api fallo (%s); fallback a playwright",
                type(e).__name__)
        reset_state()

    result = asyncio.run(main_scraper(
        today=today, hidden=hidden, date=day, select_all=select_all))
    if not result or result[1] is None:
        logger.error("no se pudieron obtener los vuelos (api intentada: %s)",
                     api_attempted)
        raise FlightsUnavailable("No se pudieron obtener los vuelos")
    logger.info("fuente de vuelos: playwright")
    return result
