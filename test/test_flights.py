import datetime
import json
import logging
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import SecretStr

from src.app import flights
from src.app.api.errors import ApiError
from src.app.models.aircraft import AirCraft

FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "bookings_20261105.json").read_text())
DAY = datetime.date(2026, 11, 5)
PASSWORD = "s3cr3t-password"


def cfg(use_api=True):
    return SimpleNamespace(
        USE_API_FIRST=use_api, user="user@example.com",
        password=SecretStr(PASSWORD), API_LOGIN_URL="https://login",
        API_BOOKINGS_URL="https://bookings", API_TIMEOUT=1,
        API_EXTRA_CA_FILE=None)


class FakeClient:
    behavior = None  # dict de respuesta o excepcion

    def __init__(self, **kwargs):
        pass

    def get_bookings(self, day):
        if isinstance(self.behavior, Exception):
            raise self.behavior
        return self.behavior


@pytest.fixture(autouse=True)
def entorno(monkeypatch):
    flights.reset_state()
    calls = {"playwright": 0, "tables": 0}

    async def fake_playwright(**kwargs):
        calls["playwright"] += 1
        # el estado debe llegar limpio al fallback
        assert AirCraft.all_reservas == {}
        return "titulo", calls.get("pw_table", "<table>pw</table>")

    def fake_series(today, date):
        calls["tables"] += 1
        calls["saved"] = {k: list(v["takeoff"])
                          for k, v in AirCraft.all_reservas.items()}
        return "serie", "file.xlsx", "<table>api</table>"

    monkeypatch.setattr(flights, "PrivateRadarClient", FakeClient)
    monkeypatch.setattr(flights, "main_scraper", fake_playwright)
    monkeypatch.setattr(flights, "clas_to_series", fake_series)
    yield calls
    flights.reset_state()


def run(c=None, **kw):
    return flights.get_flights(today=True, date=DAY, cfg=c or cfg(), **kw)


def test_api_correcta_no_abre_navegador(entorno, caplog):
    FakeClient.behavior = FIXTURE
    with caplog.at_level(logging.INFO):
        title, table = run()
    assert (title, table) == (None, "<table>api</table>")
    assert entorno["playwright"] == 0
    assert "fuente de vuelos: api" in caplog.text
    assert entorno["saved"]  # las reservas llegaron al pipeline comun


@pytest.mark.parametrize("error", [
    ApiError("login: http_401"), ApiError("bookings: timeout"),
    ApiError("schema: falta aircraftsWithBookings"), RuntimeError("raro")])
def test_fallo_de_api_activa_playwright(entorno, caplog, error):
    FakeClient.behavior = error
    with caplog.at_level(logging.INFO):
        title, table = run()
    assert table == "<table>pw</table>"
    assert entorno["playwright"] == 1
    assert "fuente de vuelos: playwright" in caplog.text
    assert "fallback a playwright" in caplog.text
    assert PASSWORD not in caplog.text


def test_esquema_inesperado_real_activa_playwright(entorno):
    FakeClient.behavior = {"otra": "cosa"}
    assert run()[1] == "<table>pw</table>"
    assert entorno["playwright"] == 1


def test_fallo_tras_guardar_no_contamina_el_fallback(entorno, monkeypatch):
    # la API devuelve datos validos, pero falla la generacion de tablas
    FakeClient.behavior = FIXTURE

    def serie_falla(today, date):
        assert AirCraft.all_reservas  # ya habia reservas acumuladas
        raise OSError("disco lleno")
    monkeypatch.setattr(flights, "clas_to_series", serie_falla)
    assert run()[1] == "<table>pw</table>"  # el fake de playwright exige estado limpio
    assert entorno["playwright"] == 1


def test_interruptor_desactivado_usa_solo_playwright(entorno):
    FakeClient.behavior = FIXTURE
    assert run(cfg(use_api=False))[1] == "<table>pw</table>"
    assert entorno["tables"] == 0


def test_ambas_fuentes_fallan(entorno, monkeypatch):
    FakeClient.behavior = ApiError("login: timeout")

    async def pw_falla(**kwargs):
        return None, None
    monkeypatch.setattr(flights, "main_scraper", pw_falla)
    with pytest.raises(flights.FlightsUnavailable):
        run()
