# Proposal

## Why

En producción, cuando un usuario pide generar los vuelos de hoy o de mañana (`POST /vuelos`), los logs no permiten saber en qué punto está el hilo: solo se ve `ver Dia ...`, el login de la API y, al final, la fuente usada. No se registra el inicio de la generación, ni cuándo se reutiliza un Excel ya existente, ni el tiempo de cada fase. Con `gunicorn -w 2 --timeout 120`, las líneas de dos peticiones se mezclan sin forma de distinguirlas, y si un worker supera los 120 s y muere (posible en el fallback a Playwright, que acumula esperas fijas de más de 30 s) no queda ningún error: el último log es un paso intermedio.

## What Changes

- Cada generación de vuelos recibe un **identificador de petición** corto que aparece en todas las líneas de log de esa generación (ruta, API, Playwright, parseo, tabla y Excel), incluidas las emitidas desde el hilo asyncio del fallback.
- Se registran el **inicio** (día, `select_all`, si el Excel existe y se reutiliza o se regenera) y el **final** (fuente usada, número de reservas y duración total) de cada petición.
- Se registran las **fases con su duración**: login y consulta a la API, parseo, guardado de reservas, generación de la tabla y de los estilos del Excel; en Playwright, cada etapa (login, calendario, filtros, lectura de reservas).
- Cuando la generación falla, la ruta registra el error **con traza** (`logger.exception`) en lugar de solo `Error {e}`.
- Se añade una línea de **aviso de progreso al pasar a Playwright**, indicando que el fallback puede tardar y cuál es el límite de gunicorn, para que una muerte del worker por timeout sea reconocible en los logs.
- Se retiran líneas de log que solo añaden ruido (`filepath`, `pdf_output`, volcado de HTML `ele: ...`).
- Ningún mensaje nuevo incluye credenciales, tokens ni el contenido de las reservas.

## Capabilities

### New Capabilities

(ninguna)

### Modified Capabilities

- `runtime-logging`: se añade un requisito de trazabilidad de la generación de vuelos (identificador de petición, inicio/fin, fases con duración, error con traza) que amplía lo que la aplicación registra al ejecutarse.

## Impact

- Código: `src/auth/routes.py` (ruta `vuelos`), `src/app/flights.py`, `src/app/api/client.py`, `src/app/api/adapter.py`, `src/app/automation/main_scraper.py`, `src/app/utils/utils.py`, `src/app/utils/styles.py`, `src/__init__.py` (formato y filtro de logging).
- Sin cambios en la API pública, la base de datos, las dependencias ni el comportamiento funcional de la generación; solo en lo que se escribe en los logs.
- Spec afectado: `openspec/specs/runtime-logging/spec.md`.

## Assumptions

- El identificador se implementa con `contextvars` y un `logging.Filter` global (no como prefijo manual), porque así lo heredan los módulos existentes sin cambiar cada llamada a `logger`.
- La limpieza de ruido de logs se incluye en este cambio por afectar a las mismas funciones.
- Fuera de alcance: persistir los logs en fichero, métricas, y cambiar el `--timeout` de gunicorn o las esperas fijas de Playwright.
