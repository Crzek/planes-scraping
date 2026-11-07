"""DATABASE_PASS no debe salir en claro al imprimir la configuracion."""
from src.core.settings import Settings


def test_database_pass_enmascarado_al_imprimir():
    s = Settings(DATABASE_PASS="s3cr3t-db")
    assert "s3cr3t-db" not in str(s)
    assert "s3cr3t-db" not in repr(s)


def test_database_url_usa_la_contrasena_real():
    s = Settings(DATABASE_USER="u", DATABASE_PASS="s3cr3t-db",
                 DATABASE_HOST="h", DATABASE_PORT="5432", DATABASE_NAME="d")
    assert s.DATABASE_URL == "postgresql://u:s3cr3t-db@h:5432/d"
