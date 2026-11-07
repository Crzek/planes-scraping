# Tasks

## 1. Estudio de viabilidad (go/no-go)

- [x] 1.2 Escribir un script desechable en la carpeta scratchpad (fuera de `src/`) que lea `user`/`password` de `.env`, haga el login y la consulta de reservas de hoy, y muestre solo la estructura de la respuesta (claves y tipos), sin imprimir contraseña ni token (verificación: el script termina con código 0 y lista las claves) — hecho el 2026-11-05: login 200 con `token`, consulta 200 para 20261105 y 20261106
- [x] 1.3 Con una respuesta real del mismo día que un Excel generado por Playwright, comparar `registration`, `timestamp_begin`/`timestamp_end` (hora Madrid), `cancel_reason` y `crew[].firstname`/`lastname` contra el Excel; confirmar si la hora coincide con la reserva o incluye el `prebrief_min` y en qué formato se muestra el nombre hoy (verificación: tabla de diferencias anotada en `design.md`; si hay discrepancias que no se pueden explicar, detener el cambio y avisar) — hecho 2026-11-07: tabla en `design.md` ("Comparación API vs Playwright"); todas las diferencias explicadas
- [x] 1.4 Guardar una respuesta de ejemplo anonimizada (sin nombres reales ni tokens) como fixture en `test/fixtures/` (verificación: el archivo no contiene emails, nombres de personas ni el token)

## 2. Configuración y dependencias

- [x] 2.1 Añadir `requests` (y `pytest` como dependencia de desarrollo) a `pyproject.toml` y regenerar `uv.lock` (verificación: `uv sync` termina sin errores e `import requests` funciona)
- [x] 2.2 Añadir a `Settings` y a `.env.example` las URLs de login y reservas de la API, el timeout y el interruptor `USE_API_FIRST` (por defecto `false` en el primer despliegue) (verificación: `Settings()` carga con y sin las variables; `.env.example` documenta cada una sin valores reales)
- [x] 2.3 Versionar `certs/sectigo-dv-r36.pem` (ya descargado y verificado), copiarlo en la imagen Docker (`Dockerfile` y `docker/`) y construir el bundle `certifi` + intermedio para `requests` (verificación: login a `api4.private-radar.com` con verificación TLS activa funciona en local y dentro del contenedor)

## 3. Cliente API y adaptador

- [x] 3.1 Crear `src/app/api/client.py` con login y consulta de reservas por fecha (`YYYYMMDD`), timeout, máx. 1 reintento en error de red y logs sin secretos (verificación: tests unitarios con respuestas simuladas cubren éxito, 401, timeout y JSON inválido)
- [x] 3.2 Crear `src/app/api/adapter.py` que valide el esquema de la respuesta (`aircraftsWithBookings[].bookings[]` con `registration`, `timestamp_begin`, `timestamp_end`, `crew`) y la convierta en registros normalizados: horas a `HH:MM` Madrid, persona desde `crew[].firstname/lastname`, descarte de reservas con `cancel_reason` no vacío, filtro DUAL/PIC por `crew[].func` (la exclusión de `No_Plane` se mantiene en un único sitio, el pipeline común `get_all_reservas`, cubierta por `test/test_utils_pipeline.py`) (verificación: test con el fixture de 1.4 que cubre reserva cancelada, reserva sin `cancel_reason`, conversión horaria y esquema inesperado que lanza el error de fallback)
- [x] 3.3 Extraer de `save_Book_by_tag` la creación de `AirCraft`/`Book` a una función reutilizable sin cambiar su comportamiento (verificación: test de caracterización que demuestra que `save_Book_by_tag` produce el mismo `AirCraft.all_reservas` que antes)

## 4. Orquestador y fallback

- [x] 4.1 Crear `get_flights(today, hidden, date, select_all)` que intente la API, limpie `AirCraft.all_reservas` ante fallo y ejecute `main_scraper` como respaldo, respetando `USE_API_FIRST` (verificación: tests que simulan éxito de API, login rechazado, timeout, esquema inesperado y fallo de ambas fuentes; en cada caso se comprueba la fuente usada y el log)
- [x] 4.2 Cambiar en `src/auth/routes.py` la llamada a `main_scraper` por `get_flights`, manteniendo la misma firma de retorno (verificación: con `USE_API_FIRST=false` la página de vuelos se genera igual que antes) — hecho 2026-11-07: con `USE_API_FIRST=false`, `get_flights` llama a `main_scraper` y genera la tabla (log `fuente de vuelos: playwright`)
- [x] 4.3 Documentar el flujo API-first, el fallback y el interruptor en `CLAUDE.md` o `Readme.md` (verificación: los comandos documentados se ejecutan tal como están escritos)

## 5. Integración

- [ ] 5.1 Con `USE_API_FIRST=true` y BD local, generar vuelos de hoy y de mañana desde la web y comparar Excel/HTML con los de Playwright (verificación: mismas filas y horas; log indica `api`)
  - 2026-11-07: generado hoy y mañana; las tablas no coinciden en todo, pero cada diferencia está explicada en `design.md`. Pendiente decidir: mostrar `PIC2` (solo) y mostrar matrícula real en reservas privadas.
- [x] 5.2 Forzar un fallo de la API (URL inválida) y repetir (verificación: se genera el mismo resultado y el log indica `playwright` con el motivo, sin credenciales) — hecho 2026-11-07: `API_LOGIN_URL` inválida → tabla idéntica a Playwright y log `api fallo (login: http_404); fallback a playwright`, sin credenciales
- [x] 5.3 Revisar que ningún log, archivo versionado ni mensaje al usuario contiene contraseña o token (verificación: `git grep` de la contraseña/prefijo de token no encuentra coincidencias y revisión del log de una ejecución) — hecho 2026-11-07 tras `fix-startup-logging-and-db-secret`: ni contraseñas, ni `SECRET_KEY`, ni JWT en logs; `git grep` sin coincidencias

## Workflow follow-up

- Activar `USE_API_FIRST=true` en producción tras comparar resultados durante unos días.
- Decidir en un cambio posterior si se retira Playwright.
- Archivar el cambio cuando se cumplan los requisitos de revisión del proyecto.
