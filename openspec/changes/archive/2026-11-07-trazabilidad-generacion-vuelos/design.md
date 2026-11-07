# Design

## Context

La generación de vuelos entra por `POST /vuelos` (`src/auth/routes.py`) y llama a `get_flights` (`src/app/flights.py`), que intenta la API (`src/app/api/client.py` + `adapter.py`) y, si falla, ejecuta Playwright con `asyncio.run(main_scraper(...))`. Después se genera la tabla (`clas_to_series`) y el Excel con estilos (`main_styles`). Ver `proposal.md` para la motivación.

Restricciones relevantes:
- Producción: `gunicorn -w 2 --timeout 120`, así que hay dos procesos worker, cada uno con una petición a la vez (worker síncrono); los logs de ambos se intercalan en `docker logs`.
- `asyncio.run` crea un event loop nuevo dentro del mismo hilo; una `ContextVar` fijada antes de `asyncio.run` se copia al contexto de las tareas del loop, por lo que se hereda.
- El logging se configura una vez en `create_app` con `basicConfig(force=True)` y formato propio. `main_scraper.py` y `src/app/main.py` llaman además a `basicConfig` a nivel de módulo (sin `force`, no tiene efecto una vez configurado el raíz).
- No hay suite de tests; la verificación es manual (ver `openspec/config.yaml`).

## Goals / Non-Goals

**Goals:**
- Poder reconstruir en `docker logs` qué hizo cada petición de generación, en qué fase está y cuánto tardó cada una.
- Que una muerte del worker por timeout sea reconocible por la última línea de esa petición.

**Non-Goals:**
- Persistir logs en fichero, enviar métricas o introducir una librería de trazas.
- Cambiar `--timeout`, las esperas fijas de Playwright o la lógica de fuentes.
- Trazar peticiones distintas de la generación de vuelos.

## Decisions

### 1. Identificador con `contextvars` + `logging.Filter` global
Un módulo pequeño (`src/core/tracing.py`) define `request_id: ContextVar[str]`, un `logging.Filter` que inyecta `record.request_id` (`-` si no hay) y un gestor de contexto `trace_request()` que fija y restablece el id. El filtro se añade al handler en `create_app` y el formato pasa a incluir `[%(request_id)s]`.

*Alternativas:* (a) prefijo manual en cada `logger.info`: obliga a pasar el id por todas las firmas y tocar decenas de líneas; (b) `flask.g`: no existe fuera del contexto de petición y no llega bien al código async; (c) `logging.LoggerAdapter`: requiere cambiar cada `getLogger`. `contextvars` no cambia las firmas y se hereda en `asyncio.run`.

### 2. El id lo crea la ruta, no `get_flights`
`trace_request()` envuelve el cuerpo del POST en la ruta `vuelos`, para que también salgan con id las líneas de la comprobación del Excel y los estilos. Id: 8 caracteres hexadecimales de `uuid4().hex`.

### 3. Fases cronometradas con un gestor de contexto `phase(nombre)`
En el mismo módulo, `phase("api.login")` mide con `time.perf_counter()` y emite `fase=<nombre> duracion=<s>s` al salir (también si hay excepción, con `fallo`). Se usa en la ruta, en `get_flights` (API, parseo, guardado, tabla) y en `main_scraper` (login, calendario, filtros, lectura). Además emite una línea de **entrada** (`fase=<nombre> inicio`) en INFO para todas las fases: es la que permite identificar la fase en curso si el worker muere sin llegar a escribir la de salida.

*Alternativa:* un decorador. Descartado porque varias fases son bloques dentro de una función, no funciones completas.

### 4. Aviso del límite de tiempo
`get_flights` lee la variable de entorno `TIMEOUT` (la misma que usa `entrypoint.sh` para `--timeout`, por defecto 120) y la imprime en el aviso del fallback. Es solo informativo; no se aplica ningún límite desde la app y no se añade ningún ajuste nuevo. *Alternativa:* pedir el valor real al arbiter de gunicorn en ejecución; descartado por complejidad.

### 5. Traza en la ruta
En el `except` de la ruta se sustituye `logger.error(f"Error {e}")` por `logger.exception("generacion de vuelos fallo")`. La respuesta HTML no cambia.

### 6. Limpieza de ruido
Se eliminan `filepath`, `pdf_output` (ruta) y `ele: {html_str}` (HTML volcado) en `src/auth/routes.py` y `src/app/main.py`. Las líneas de `print`/`logger.info` de la clase `Book`/`Aircraft` quedan fuera salvo que contengan datos de personas, en cuyo caso se pasan a DEBUG o se quitan (se revisa en la implementación).

## Risks / Trade-offs

- [`ContextVar` no se hereda a hilos creados con `threading` o `run_in_executor` sin copiar contexto] → hoy no hay ninguno en el flujo; se comprueba con una verificación manual del fallback.
- [Dos `basicConfig` a nivel de módulo en `main_scraper.py` y `main.py`] → no tienen efecto una vez configurado el raíz con `force=True`; se dejan, pero el filtro vive en el handler del raíz y no depende de ellos.
- [Más líneas INFO por petición (~15)] → volumen bajo (peticiones manuales ocasionales); aceptable.
- [Un worker muerto por SIGKILL no escribe nada al morir] → por eso la línea de *inicio* de fase es necesaria: la última línea con ese id nombra la fase atascada.
- [El id aparece en el formato global] → las líneas ajenas a una petición muestran `-`; se cambia el formato de todos los logs, no solo los de vuelos.

## Open Questions

- ¿Conviene exponer el id de petición también en la página de error para que el usuario lo comunique al soporte? No bloquea; puede añadirse luego sin cambiar los specs.
