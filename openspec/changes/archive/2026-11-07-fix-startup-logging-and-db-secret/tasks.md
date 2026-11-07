# Tasks

## 1. Logging

- [x] 1.1 En `src/__init__.py`, mover `logging.basicConfig(level=INFO, ..., force=True)` al inicio de `create_app()`; añadir test en `test/test_logging_config.py` que llame a `create_app()` y compruebe que el raíz queda en INFO (verificación: `uv run pytest test/test_logging_config.py` pasa)

## 2. Secreto de la base de datos

- [x] 2.1 `DATABASE_PASS: SecretStr` en `src/core/settings.py`, `get_secret_value()` en `DATABASE_URL` y en `src/config/default.py`; test que compruebe que `str(Settings(DATABASE_PASS="s3cr3t"))` no contiene `s3cr3t` y `DATABASE_URL` sí (verificación: `uv run pytest` pasa)
- [x] 2.2 `test_intermedio_del_repo_es_valido` hace `pytest.skip` si no existe `certs/sectigo-dv-r36.pem` (verificación: `uv run pytest` pasa sin `certs/` y con `certs/`)

## 3. Verificación en Docker y docs

- [x] 3.1 Levantar `docker-compose.yml` + `docker-compose.db.yml` en local y comprobar en `docker logs prod-planes-pw`: aparece `***** Inicio de la app *****` y `DB connection: OK`, y no aparece el valor de `DATABASE_PASS`
- [x] 3.2 Quitar del README las mejoras pendientes 1 y 2 (resueltas) y actualizar la referencia de la tarea 1.5 del despliegue del certificado (verificación: `grep -n "Mejoras pendientes" -A5 Readme.md`)
