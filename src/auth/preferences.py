"""Valores por defecto, validacion y normalizacion de las preferencias de la tabla.

Funciones puras (sin Flask ni base de datos) para poder probarlas aisladas.
"""
from src.core.settings import settings

MAX_PLANES = 500
MAX_PLANE_LEN = 32


def default_preferences() -> dict:
    """Rango por defecto: el que antes estaba fijo (START_DEL..24-END_DEL-1)."""
    return {
        "hour_start": settings.START_DEL,
        "hour_end": 24 - 1 - settings.END_DEL,
        "hidden_planes": [],
    }


def _as_hour(value):
    # bool es subclase de int: no vale como hora
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value if 0 <= value <= 23 else None


def validate_preferences(payload) -> tuple[dict | None, dict]:
    """Valida y normaliza un payload.

    Returns:
        (datos normalizados, errores por campo). Si hay errores, datos es None.
    """
    errors: dict[str, str] = {}
    if not isinstance(payload, dict):
        return None, {"_": "El cuerpo debe ser un objeto JSON"}

    start = _as_hour(payload.get("hour_start"))
    end = _as_hour(payload.get("hour_end"))
    if start is None:
        errors["hour_start"] = "La hora inicial debe ser un entero entre 0 y 23"
    if end is None:
        errors["hour_end"] = "La hora final debe ser un entero entre 0 y 23"
    if not errors and start > end:
        errors["hour_start"] = (
            "La hora inicial no puede ser mayor que la hora final")

    planes = payload.get("hidden_planes", [])
    cleaned: list[str] = []
    if not isinstance(planes, list) or len(planes) > MAX_PLANES:
        errors["hidden_planes"] = "Debe ser una lista de matrículas"
    else:
        for plane in planes:
            if not isinstance(plane, str):
                errors["hidden_planes"] = "Cada matrícula debe ser texto"
                break
            plane = plane.strip()
            if not plane or len(plane) > MAX_PLANE_LEN:
                errors["hidden_planes"] = (
                    f"Cada matrícula debe tener entre 1 y {MAX_PLANE_LEN} caracteres")
                break
            if plane not in cleaned:
                cleaned.append(plane)

    if errors:
        return None, errors
    return {"hour_start": start, "hour_end": end,
            "hidden_planes": cleaned}, {}
