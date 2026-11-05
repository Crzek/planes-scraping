from datetime import date
from unittest.mock import MagicMock

import pytest
import requests

from src.app.api.client import (
    PrivateRadarClient, build_ca_bundle, build_payload)
from src.app.api.errors import ApiError

PASSWORD = "s3cr3t-password"
TOKEN = "eyJ.fake.token"


def make_response(status=200, json_data=None, bad_json=False):
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status
    resp.ok = status < 400
    if bad_json:
        resp.json.side_effect = ValueError("no json")
    else:
        resp.json.return_value = json_data
    return resp


def make_client(*post_effects):
    session = MagicMock()
    session.headers = {}
    session.post.side_effect = list(post_effects)
    client = PrivateRadarClient(
        "user@example.com", PASSWORD, "https://login", "https://bookings",
        timeout=3, extra_ca_file=None, session=session)
    return client, session


def test_payload_fecha_en_formato_yyyymmdd():
    payload = build_payload(date(2026, 11, 6))
    assert payload["strDate"] == 20261106
    assert payload["period"] == "D"


def test_exito_login_y_reservas():
    data = {"aircraftsWithBookings": []}
    client, session = make_client(
        make_response(json_data={"token": TOKEN}),
        make_response(json_data=data))
    assert client.get_bookings(date(2026, 11, 5)) == data
    login_call, bookings_call = session.post.call_args_list
    assert login_call.kwargs["json"] == {
        "email": "user@example.com", "password": PASSWORD}
    assert bookings_call.kwargs["headers"] == {"Authorization": TOKEN}
    assert bookings_call.kwargs["timeout"] == 3


@pytest.mark.parametrize("status", [401, 403, 500])
def test_login_rechazado(status):
    client, _ = make_client(make_response(status=status))
    with pytest.raises(ApiError, match=f"login: http_{status}"):
        client.login()


def test_timeout_no_reintenta():
    client, session = make_client(requests.exceptions.Timeout())
    with pytest.raises(ApiError, match="login: timeout"):
        client.login()
    assert session.post.call_count == 1


def test_error_de_conexion_reintenta_una_vez():
    client, session = make_client(
        requests.exceptions.ConnectionError(),
        make_response(json_data={"token": TOKEN}))
    client.login()
    assert session.post.call_count == 2


def test_error_de_conexion_persistente():
    client, session = make_client(
        requests.exceptions.ConnectionError(),
        requests.exceptions.ConnectionError())
    with pytest.raises(ApiError, match="connection_error"):
        client.login()
    assert session.post.call_count == 2


def test_error_tls():
    client, _ = make_client(requests.exceptions.SSLError("detalle"))
    with pytest.raises(ApiError, match="tls_error"):
        client.login()


def test_json_invalido_en_login():
    client, _ = make_client(make_response(bad_json=True))
    with pytest.raises(ApiError, match="login: invalid_json"):
        client.login()


def test_login_sin_token():
    client, _ = make_client(make_response(json_data={"status": "ok"}))
    with pytest.raises(ApiError, match="login: no_token"):
        client.login()


def test_json_invalido_en_reservas():
    client, _ = make_client(
        make_response(json_data={"token": TOKEN}),
        make_response(bad_json=True))
    with pytest.raises(ApiError, match="bookings: invalid_json"):
        client.get_bookings(date(2026, 11, 5))


def test_el_error_y_los_logs_no_contienen_secretos(caplog):
    client, _ = make_client(
        make_response(json_data={"token": TOKEN}),
        make_response(status=401))
    with caplog.at_level("DEBUG"):
        with pytest.raises(ApiError) as exc:
            client.get_bookings(date(2026, 11, 5))
    visible = str(exc.value) + caplog.text
    assert PASSWORD not in visible and TOKEN not in visible


def test_bundle_incluye_intermedio_y_certifi(tmp_path):
    extra = tmp_path / "extra.pem"
    extra.write_text("-----BEGIN CERTIFICATE-----\nEXTRA\n-----END CERTIFICATE-----\n")
    bundle = build_ca_bundle(str(extra))
    text = open(bundle).read()
    assert "EXTRA" in text and text.count("BEGIN CERTIFICATE") > 10


def test_bundle_con_fichero_inexistente():
    with pytest.raises(ApiError, match="ca_file_missing"):
        build_ca_bundle("no/existe.pem")


def test_intermedio_del_repo_es_valido():
    import ssl
    from pathlib import Path
    pem = Path("certs/sectigo-dv-r36.pem").read_text()
    assert ssl.PEM_cert_to_DER_cert(pem)
