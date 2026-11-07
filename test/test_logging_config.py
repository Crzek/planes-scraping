"""create_app deja el logging raiz en INFO aunque algo loguee antes."""
import logging

import pytest


@pytest.fixture
def sin_bd_real(monkeypatch):
    # puerto cerrado en localhost: la conexion falla al instante y no toca
    # ninguna base de datos real del .env
    monkeypatch.setenv("DATABASE_HOST", "127.0.0.1")
    monkeypatch.setenv("DATABASE_PORT", "1")


def test_create_app_configura_logging_info(sin_bd_real, monkeypatch):
    root = logging.getLogger()
    monkeypatch.setattr(root, "handlers", [])
    monkeypatch.setattr(root, "level", logging.WARNING)
    # simula una llamada a logging antes de configurar (el bug original)
    logging.warning("log previo a create_app")

    from src import create_app
    create_app()

    assert logging.getLogger().getEffectiveLevel() == logging.INFO
