## 1. Infraestructura de trazabilidad

- [x] 1.1 Crear `src/core/tracing.py` con `request_id` (`ContextVar`), `RequestIdFilter`, `trace_request()` (id de 8 hex, restablece al salir) y `phase(nombre)` (línea de inicio y línea de fin con duración, también si hay excepción)
- [x] 1.2 En `create_app` (`src/__init__.py`) añadir el filtro al handler del raíz e incluir `[%(request_id)s]` en el formato; comprobar que las líneas de arranque salen con `-`

## 2. Ruta de generación

- [x] 2.1 En `vuelos` (`src/auth/routes.py`) envolver el POST con `trace_request()` y registrar la línea de inicio (día, `select_all`, Excel existente: reutiliza/regenera) y la de fin (resultado, fuente, nº de reservas, duración total)
- [x] 2.2 Registrar con `phase("excel.estilos")` la llamada a `main_styles`
- [x] 2.3 Sustituir `logger.error(f"Error {e}")` por `logger.exception(...)` sin cambiar el mensaje que ve el usuario
- [x] 2.4 Quitar los logs de ruido `--filepath---` y `pdf_output ----`

## 3. Fuentes de vuelos

- [x] 3.1 En `src/app/flights.py` envolver con `phase()` login/consulta de la API, parseo, guardado de reservas y `clas_to_series`
- [x] 3.2 Al caer al fallback, registrar un aviso con el motivo y el límite de tiempo leído de `TIMEOUT` (por defecto 120)
- [x] 3.3 Devolver o registrar el número de reservas y la fuente usada para la línea de fin de la ruta
- [x] 3.4 En `src/app/automation/main_scraper.py` envolver con `phase()` login, calendario, filtros y lectura de reservas
- [x] 3.5 Quitar el volcado `ele: {html_str}` en `src/app/main.py` y revisar que ningún log nuevo o existente de la generación incluya nombres de personas, tokens o credenciales

## 4. Verificación manual

- [x] 4.1 Con `USE_API_FIRST=true`, generar mañana y comprobar en el log: inicio, fases con duración, fin con fuente `api` y el mismo id en todas las líneas
- [x] 4.2 Forzar fallo de la API (credenciales o URL erróneas) y comprobar el aviso de fallback, las etapas de Playwright con el mismo id y la fuente `playwright`
- [x] 4.3 Pedir un día cuyo Excel ya existe y comprobar la línea de reutilización
- [x] 4.4 Forzar una excepción y comprobar la traza en el log y el mensaje sin traza en la página
- [x] 4.5 Lanzar dos generaciones simultáneas y comprobar que los ids son distintos
- [x] 4.6 Revisar `docker logs` completo y confirmar que no aparecen la contraseña, el token ni HTML
