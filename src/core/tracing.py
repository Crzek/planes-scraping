"""Trazabilidad de la generacion de vuelos: id de peticion y fases con duracion."""
import contextlib
import contextvars
import logging
import time
import uuid

request_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-")

# datos de resumen de la generacion en curso (fuente, reservas) y su inicio
outcome: contextvars.ContextVar[dict] = contextvars.ContextVar(
    "outcome", default=None)

logger = logging.getLogger("tracing")


class RequestIdFilter(logging.Filter):
    """Inyecta ``record.request_id`` (``-`` fuera de una generacion)."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id.get()
        return True


@contextlib.contextmanager
def trace_request():
    """Asigna un id corto a la generacion en curso y lo restablece al salir."""
    token = request_id.set(uuid.uuid4().hex[:8])
    data = {"start": time.perf_counter()}
    token_outcome = outcome.set(data)
    try:
        yield data
    finally:
        outcome.reset(token_outcome)
        request_id.reset(token)


def note(**values) -> None:
    """Anota datos de resumen (fuente, reservas) de la generacion en curso."""
    data = outcome.get()
    if data is not None:
        data.update(values)


def elapsed(data: dict) -> float:
    """Segundos transcurridos desde el inicio de la generacion."""
    return time.perf_counter() - data["start"]


@contextlib.contextmanager
def phase(name: str):
    """Registra inicio y fin (con duracion) de una fase, tambien si falla.

    La linea de inicio permite saber que fase estaba en curso si el worker
    muere por timeout sin llegar a escribir la de fin.
    """
    logger.info("fase=%s inicio", name)
    start = time.perf_counter()
    try:
        yield
    except BaseException:
        logger.warning("fase=%s fallo duracion=%.1fs",
                       name, time.perf_counter() - start)
        raise
    logger.info("fase=%s fin duracion=%.1fs",
                name, time.perf_counter() - start)
