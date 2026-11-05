"""Convierte la respuesta de getByFilterNew en reservas normalizadas."""
import logging
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from src.app.api.errors import ApiError

logger = logging.getLogger(__name__)

TZ = ZoneInfo("Europe/Madrid")
# Misma regla que el flujo Playwright: '"DUAL" in info or "PIC" in info'
# (subcadena), por lo que PIC2, SPIC o PICUS tambien pasan el filtro.
ROLE_MARKERS = ("DUAL", "PIC")


@dataclass(frozen=True)
class FlightBooking:
    registration: str
    takeoff: str  # HH:MM, hora de Madrid
    landing: str  # HH:MM, hora de Madrid
    person: str
    roles: tuple[str, ...]


def _hhmm(epoch_ms: int) -> str:
    return datetime.fromtimestamp(epoch_ms / 1000, TZ).strftime("%H:%M")


def _is_cancelled(booking: dict) -> bool:
    reason = booking.get("cancel_reason")
    return isinstance(reason, str) and reason.strip() != ""


def _has_role(crew: list[dict]) -> bool:
    return any(marker in str(member.get("func", ""))
               for member in crew for marker in ROLE_MARKERS)


def _person(crew: list[dict]) -> str:
    names = (f"{m.get('firstname', '')} {m.get('lastname', '')}".strip()
             for m in crew)
    return ", ".join(n for n in names if n)


def _validated(booking: object, where: str) -> dict:
    if not isinstance(booking, dict):
        raise ApiError(f"schema: {where} no es un objeto")
    if not isinstance(booking.get("registration"), str) \
            or not booking["registration"]:
        raise ApiError(f"schema: {where} sin registration")
    for key in ("timestamp_begin", "timestamp_end"):
        value = booking.get(key)
        if isinstance(value, bool) or not isinstance(value, int):
            raise ApiError(f"schema: {where} sin {key}")
    if not isinstance(booking.get("crew"), list):
        raise ApiError(f"schema: {where} sin crew")
    return booking


def parse_bookings(response: dict) -> list[FlightBooking]:
    """Valida el esquema y devuelve las reservas activas con rol DUAL/PIC.

    Lanza ApiError si el esquema no es el esperado o si no queda ninguna
    reserva utilizable (en ambos casos se debe usar el fallback).
    """
    aircrafts = response.get("aircraftsWithBookings") \
        if isinstance(response, dict) else None
    if not isinstance(aircrafts, list):
        raise ApiError("schema: falta aircraftsWithBookings")

    result: list[FlightBooking] = []
    total = 0
    for a_idx, aircraft in enumerate(aircrafts):
        bookings = aircraft.get("bookings") if isinstance(aircraft, dict) \
            else None
        if not isinstance(bookings, list):
            raise ApiError(f"schema: aircraft[{a_idx}] sin bookings")
        for b_idx, raw in enumerate(bookings):
            booking = _validated(raw, f"aircraft[{a_idx}].bookings[{b_idx}]")
            total += 1
            if _is_cancelled(booking) or not _has_role(booking["crew"]):
                continue
            result.append(FlightBooking(
                registration=booking["registration"],
                takeoff=_hhmm(booking["timestamp_begin"]),
                landing=_hhmm(booking["timestamp_end"]),
                person=_person(booking["crew"]),
                roles=tuple(str(m.get("func", "")) for m in booking["crew"]),
            ))

    if not result:
        raise ApiError(f"schema: sin reservas utilizables (total={total})")
    logger.info("API: %s reservas recibidas, %s utilizables", total,
                len(result))
    return result
