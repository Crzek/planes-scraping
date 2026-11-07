import json
from pathlib import Path

import pytest

from src.app.api.adapter import FlightBooking, parse_bookings
from src.app.api.errors import ApiError

FIXTURES = Path(__file__).parent / "fixtures"
MS_2026_11_05_0800_UTC = 1793865600000  # 09:00 en Madrid (UTC+1)
MS_2026_07_01_0800_UTC = 1782892800000  # 10:00 en Madrid (UTC+2, verano)


def load(day):
    return json.loads((FIXTURES / f"bookings_{day}.json").read_text())


def booking(**over):
    base = {
        "registration": "EC-AAA",
        "timestamp_begin": MS_2026_11_05_0800_UTC,
        "timestamp_end": MS_2026_11_05_0800_UTC + 90 * 60 * 1000,
        "crew": [{"func": "DUAL", "firstname": "Ana", "lastname": "Uno"},
                 {"func": "PIC", "firstname": "Luis", "lastname": "Dos"}],
    }
    base.update(over)
    return base


def resp(*bookings):
    return {"aircraftsWithBookings": [{"bookings": list(bookings)}]}


def test_hora_de_madrid_invierno_utc_mas_1():
    r = parse_bookings(resp(booking()))[0]
    assert (r.takeoff, r.landing) == ("09:00", "10:30")


def test_hora_de_madrid_verano_utc_mas_2():
    r = parse_bookings(resp(booking(
        timestamp_begin=MS_2026_07_01_0800_UTC,
        timestamp_end=MS_2026_07_01_0800_UTC + 60 * 60 * 1000)))[0]
    assert (r.takeoff, r.landing) == ("10:00", "11:00")


def test_persona_desde_crew():
    r = parse_bookings(resp(booking()))[0]
    assert r.person == "Ana Uno, Luis Dos"
    assert r.roles == ("DUAL", "PIC")


def test_cancelada_se_descarta():
    data = resp(booking(cancel_reason="Weather"), booking(registration="EC-BBB"))
    assert [r.registration for r in parse_bookings(data)] == ["EC-BBB"]


@pytest.mark.parametrize("reason", [None, "", "  "])
def test_sin_motivo_de_cancelacion_se_incluye(reason):
    b = booking()
    if reason is not None:
        b["cancel_reason"] = reason
    assert len(parse_bookings(resp(b))) == 1


def test_filtro_por_subcadena_como_playwright():
    pic2 = booking(crew=[{"func": "PIC2", "firstname": "A", "lastname": "B"}])
    super_only = booking(crew=[{"func": "SUPER", "firstname": "A", "lastname": "B"}])
    out = parse_bookings(resp(pic2, super_only, booking(registration="EC-OK")))
    assert [r.registration for r in out] == ["PB-EC-AAA", "EC-OK"]
    assert out[0].roles == ("PIC2",)


@pytest.mark.parametrize("bad", [
    {}, {"aircraftsWithBookings": None}, [], "texto",
    {"aircraftsWithBookings": [{"sin": "bookings"}]},
    resp({"registration": "EC-A"}),
    resp(booking(timestamp_begin="09:00")),
    resp(booking(timestamp_end=None)),
    resp(booking(crew=None)),
    resp(booking(registration="")),
])
def test_esquema_inesperado_lanza_api_error(bad):
    with pytest.raises(ApiError, match="schema"):
        parse_bookings(bad)


def test_sin_reservas_utilizables_lanza_api_error():
    with pytest.raises(ApiError, match="sin reservas utilizables"):
        parse_bookings(resp(booking(cancel_reason="O")))
    with pytest.raises(ApiError):
        parse_bookings({"aircraftsWithBookings": []})


def test_fixture_dia_5_cuenta_reservas():
    out = parse_bookings(load("20261105"))
    assert len(out) == 32  # 47 reservas - 15 canceladas
    assert all(isinstance(r, FlightBooking) for r in out)
    assert "09:00" in {r.takeoff for r in out}


def test_fixture_dia_6_incluye_pic2():
    out = parse_bookings(load("20261106"))
    assert len(out) == 38  # 48 reservas - 10 canceladas
    assert any(r.roles == ("PIC2",) for r in out)
