# Design

## Context

`create_app()` (`src/__init__.py`) configura `logging.basicConfig(level=INFO, ...)` y a continuación ejecuta `print("*********Incico APP *********")` y `print_settings()`. Esta última (`src/core/settings.py`) hace `print(Settings())`: salida cruda a stdout, sin formato de logging. `Settings` es un `BaseSettings` de pydantic que ya expone `DEBUG` (en producción `False`, y `PROD = not DEBUG`). Los secretos son `SecretStr`, pero `user`, `DATABASE_HOST` y rutas salen en claro. Requisitos de enmascarado ya existentes en `runtime-logging` no cambian.

## Goals / Non-Goals

**Goals:**
- La configuración deja de imprimirse con `print` y pasa por `logging`.
- Solo se emite con `DEBUG=True` o `PRINT_SETTINGS=true`.

**Non-Goals:**
- Enmascarar `user` u otros campos no secretos (si hace falta, cambio aparte).
- Tocar el `print("*********Incico APP *********")` ni el resto de logs de arranque.
- Cambiar cómo se calcula `DEBUG`/`PROD`.

## Decisions

1. **Condición basada en `Settings.DEBUG` o un nuevo `PRINT_SETTINGS: bool = False`.** Se reutiliza `DEBUG` por ser lo que ya distingue desarrollo de producción. Alternativa: usar `FLASK_ENV`/`CONFIG_ENV`, descartada porque `DEBUG` es lo que ya gobierna `app.config["DEBUG"]` y evita dos fuentes de verdad.
2. **`print_settings()` recibe/crea un `Settings` y hace `logger.info(...)`, no `logger.debug`.** El nivel raíz es INFO; con `debug` no se vería nunca ni en desarrollo sin tocar la config. La condición ya acota cuándo sale, así que el nivel INFO no genera ruido en producción.
3. **El filtrado vive dentro de `print_settings()`** (retorna sin hacer nada si no procede), de forma que `create_app()` mantiene una sola llamada y no duplica la condición. Se evita instanciar `Settings()` dos veces reutilizando `settings_obj` al moverla tras su creación.
4. **`PRINT_SETTINGS` se documenta en `.env.example`** con valor `False`.

## Risks / Trade-offs

- [En producción con el flag activo siguen saliendo `user`, host de BD y rutas] → es opt-in y temporal; se anota en `.env.example` que debe desactivarse tras diagnosticar.
- [`extra="allow"` en `Settings` hace que una variable `PRINT_SETTINGS` mal escrita se ignore silenciosamente] → declararla como campo tipado y verificar el arranque con y sin ella.
- [Una instancia de `Settings` creada antes de `load_env()` podría no ver variables cargadas desde otro fichero] → ubicar la llamada después de `load_env()` y de crear `settings_obj`.
