"""Cliente HTTP de la API de private-radar: login y reservas de un dia."""
import logging
import tempfile
from datetime import date
from functools import lru_cache
from pathlib import Path

import certifi
import requests

from src.app.api.errors import ApiError

logger = logging.getLogger(__name__)

BOOKING_TYPES = (
    "canceled,solo,solo_sup,instr,mcc,type_rating,exam,tourist,discovery,"
    "check,ferry,trip,rental,tow,aoc,class,class-exam"
)
ORIGIN = "https://acbs.private-radar.com"
USER_AGENT = "planes-scraping/1.0"
PROJECT_ROOT = Path(__file__).resolve().parents[3]


@lru_cache(maxsize=None)
def build_ca_bundle(extra_ca_file: str | None) -> str | bool:
    """Devuelve el valor para ``verify=`` de requests.

    api4.private-radar.com no envia el certificado intermedio, asi que se
    anaden las CAs de certifi mas ese intermedio en un unico bundle. La
    verificacion TLS permanece activa. Sin fichero extra se usa certifi.
    """
    if not extra_ca_file:
        return certifi.where()
    extra = Path(extra_ca_file)
    if not extra.is_absolute():
        extra = PROJECT_ROOT / extra
    if not extra.is_file():
        raise ApiError("ca_file_missing")
    bundle = tempfile.NamedTemporaryFile(
        "w", suffix=".pem", prefix="pr-ca-", delete=False)
    with bundle:
        bundle.write(Path(certifi.where()).read_text())
        bundle.write("\n")
        bundle.write(extra.read_text())
    return bundle.name


def build_payload(day: date) -> dict:
    """Cuerpo de getByFilterNew para un dia. Sin filtros de usuario/avion."""
    return {
        "smartFilterName": "", "view_compact": False, "minh": 0, "maxh": 24,
        "bases": "", "baseView": "A", "bookingTypes": BOOKING_TYPES,
        "aircraft": "", "aircraftView": "A", "aircraftModels": "",
        "aircraftRegistrations": "", "flightInstructors": "",
        "flightInstructorView": "A", "mccInstructors": "",
        "mccInstructorView": "A", "theoryInstructors": "",
        "theoryInstructorView": "A", "otherUsers": "", "users": "",
        "classrooms": "", "classroomView": "A", "hiddenSections": [],
        "strDate": int(day.strftime("%Y%m%d")), "period": "D",
    }


class PrivateRadarClient:
    """Login + consulta de reservas. El token vive solo en memoria."""

    def __init__(
        self,
        email: str,
        password: str,
        login_url: str,
        bookings_url: str,
        timeout: float = 15.0,
        extra_ca_file: str | None = None,
        session: requests.Session | None = None,
    ):
        self._email = email
        self._password = password
        self._login_url = login_url
        self._bookings_url = bookings_url
        self._timeout = timeout
        self._token: str | None = None
        self._session = session or requests.Session()
        self._session.verify = build_ca_bundle(extra_ca_file)
        self._session.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": ORIGIN,
            "Referer": ORIGIN + "/",
            "User-Agent": USER_AGENT,
        })

    def _post(self, url: str, step: str, **kwargs) -> requests.Response:
        """POST con timeout y un unico reintento ante error de conexion."""
        last_reason = "network_error"
        for attempt in (1, 2):
            try:
                resp = self._session.post(
                    url, timeout=self._timeout, **kwargs)
            except requests.exceptions.SSLError:
                raise ApiError(f"{step}: tls_error") from None
            except requests.exceptions.Timeout:
                raise ApiError(f"{step}: timeout") from None
            except requests.exceptions.ConnectionError:
                last_reason = "connection_error"
                logger.warning("%s: error de conexion (intento %s)",
                               step, attempt)
                continue
            except requests.exceptions.RequestException:
                raise ApiError(f"{step}: request_error") from None
            if resp.status_code in (401, 403):
                raise ApiError(f"{step}: http_{resp.status_code}")
            if not resp.ok:
                raise ApiError(f"{step}: http_{resp.status_code}")
            return resp
        raise ApiError(f"{step}: {last_reason}")

    @staticmethod
    def _json(resp: requests.Response, step: str) -> dict:
        try:
            data = resp.json()
        except ValueError:
            raise ApiError(f"{step}: invalid_json") from None
        if not isinstance(data, dict):
            raise ApiError(f"{step}: unexpected_json")
        return data

    def login(self) -> None:
        resp = self._post(
            self._login_url, "login",
            json={"email": self._email, "password": self._password})
        token = self._json(resp, "login").get("token")
        if not isinstance(token, str) or not token:
            raise ApiError("login: no_token")
        self._token = token
        logger.info("login API correcto")

    def get_bookings(self, day: date) -> dict:
        """Reservas del dia. Hace login si aun no hay token."""
        if self._token is None:
            self.login()
        resp = self._post(
            self._bookings_url, "bookings",
            json=build_payload(day),
            headers={"Authorization": self._token})
        return self._json(resp, "bookings")
