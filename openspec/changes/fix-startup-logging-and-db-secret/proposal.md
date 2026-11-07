# Proposal

## Why

Al probar `download-private-radar-ca-at-docker-build` se vio que en `docker logs` no aparece ningún `logger.info` de la app (ni `fuente de vuelos: api|playwright`), y que al arrancar se imprime `DATABASE_PASS` en claro. Lo primero impide saber de dónde salen los vuelos; lo segundo deja la contraseña de la base de datos de producción en los logs del servidor. Bloquean la tarea 1.5 de `download-private-radar-ca-at-docker-build` y la 5.3 de `api-first-scraper-with-playwright-fallback`.

## What Changes

- El logging de la app se configura a nivel INFO al principio de `create_app()`, antes de cualquier llamada a `logging`. Hoy `create_static_directories()` llama a `logging.info` antes del `basicConfig`, lo que deja el logger raíz en WARNING.
- `DATABASE_PASS` pasa a ser secreto (`SecretStr`): la impresión de la configuración al arrancar lo muestra enmascarado; la URI de la base de datos sigue usando el valor real.
- El test que valida el certificado intermedio local (`test/test_api_client.py::test_intermedio_del_repo_es_valido`) se salta cuando `certs/` no existe, porque desde el cambio anterior el certificado ya no se versiona.
- README: se quitan las mejoras pendientes 1 y 2 (quedan resueltas).

Fuera de alcance: la mejora 3 (ficheros `pr-ca-*.pem` en `/tmp`) y quitar los `basicConfig` de módulos usados como scripts (`src/app/main.py`, `src/app/automation/main_scraper.py`).

## Capabilities

### New Capabilities
- `runtime-logging`: qué registra la aplicación al ejecutarse (nivel, mensajes de fuente de vuelos) y qué datos sensibles nunca deben salir en los logs.

### Modified Capabilities
<!-- Ninguna: no hay specs principales en openspec/specs/. -->

## Impact

- Código: `src/__init__.py`, `src/core/settings.py`, `test/test_api_client.py`; tests nuevos en `test/`.
- Docs: `Readme.md`.
- Tras desplegar: los logs de producción tendrán más líneas (INFO). La contraseña de la base de datos ya filtrada en logs antiguos sigue ahí; valorar rotarla.
