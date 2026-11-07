# Tasks

## 1. Registrar la configuración condicionalmente

- [x] 1.1 Añadir `PRINT_SETTINGS: bool = False` a `Settings` en `src/core/settings.py`; verificar con `uv run python -c "from src.core.settings import Settings; print(Settings().PRINT_SETTINGS)"` que devuelve `False` por defecto y `True` con `PRINT_SETTINGS=true`.
- [x] 1.2 Reescribir `print_settings()` para usar `logging.getLogger(__name__).info(...)` y salir sin emitir nada salvo que `DEBUG` o `PRINT_SETTINGS` sean verdaderos; verificar leyendo el código que ya no contiene `print(`.
- [x] 1.3 En `create_app()` (`src/__init__.py`) llamar a `print_settings` después de `load_env()` y de crear `settings_obj`, reutilizando esa instancia; verificar que el arranque sigue funcionando.

## 2. Configuración y verificación

- [x] 2.1 Documentar `PRINT_SETTINGS=False` en `.env.example` con un comentario de que es solo para diagnóstico; verificar que el fichero lo contiene.
- [x] 2.2 Verificar manualmente los tres escenarios del spec arrancando la app: con `DEBUG=True` aparece la línea con hora y nivel; con `DEBUG=False` sin flag no aparece ninguna línea con `DATABASE_HOST=`; con `DEBUG=False PRINT_SETTINGS=true` aparece y `DATABASE_PASS`/`SECRET_KEY`/`password` salen como `**********`.
