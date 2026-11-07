# Design

## Context

- `src/__init__.py::create_app()` llama a `create_static_directories()`, que hace `logging.info(...)` antes de `logging.basicConfig(level=INFO)`. La primera llamada a `logging.info` sin handlers configura el raíz en WARNING y el `basicConfig` posterior no hace nada (comprobado en el contenedor: nivel 30, origen `src/__init__.py:21`).
- `print_settings()` (`src/core/settings.py`) hace `print(Settings())`. Los campos `SecretStr` salen como `**********`; `DATABASE_PASS` es `str` y sale en claro.
- `DATABASE_PASS` se usa en `Settings.DATABASE_URL` y en `src/config/default.py::_build_postgres_uri_from_parts` (solo para comprobar que no está vacío).

## Goals / Non-Goals

**Goals:** ver INFO en `docker logs`; que `DATABASE_PASS` nunca salga en claro.

**Non-Goals:** cambiar formato de logs, quitar `print_settings`, tocar los `basicConfig` de `src/app/main.py` y `src/app/automation/main_scraper.py` (con la configuración temprana pasan a ser no-op).

## Decisions

1. **`logging.basicConfig(..., force=True)` como primera instrucción de `create_app()`.** `force=True` reemplaza cualquier handler que una llamada previa (de la app o de una librería) haya puesto en el raíz, así el nivel INFO queda garantizado. Alternativa descartada: solo mover el `basicConfig`, que depende de que nadie más loguee antes.
2. **`DATABASE_PASS: SecretStr`** y `get_secret_value()` en `DATABASE_URL`. Mismo patrón que `SECRET_KEY` y `password`. En `src/config/default.py` el `all([...])` sigue funcionando (un `SecretStr` no vacío es truthy); se cambia a `get_secret_value()` para que la comprobación de vacío sea real.
3. **Test del certificado local con `pytest.skip`** si `certs/sectigo-dv-r36.pem` no existe, en vez de borrarlo: sigue validando la copia local cuando está.

## Risks / Trade-offs

- [Más volumen de logs INFO en producción] → aceptado; son pocas líneas por petición.
- [`SecretStr` vacío: `SecretStr("")` es truthy] → por eso se usa `get_secret_value()` en el `all([...])`.
- [Contraseña ya filtrada en logs antiguos del servidor] → fuera del código; se recomienda rotarla.
