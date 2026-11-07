# Proposal

## Why

Al arrancar, `create_app()` llama a `print_settings()`, que hace un `print(Settings())` sin hora ni nivel y vuelca toda la configuración en los logs de producción. Aunque los secretos salen enmascarados (`SecretStr`), se exponen datos que no aportan en producción: el email de login de private-radar (`user`), el host de la BD y rutas internas. Es ruido y superficie de fuga innecesaria.

## What Changes

- Sustituir el `print` de la configuración por una llamada de `logging` (con hora, nivel y módulo, como el resto de logs).
- Emitir la configuración solo en modo desarrollo (`DEBUG=True`).
- En producción no emitirla por defecto, pero permitir activarla con una variable de entorno `PRINT_SETTINGS=true` para diagnóstico puntual.
- Documentar `PRINT_SETTINGS` en `.env.example`.

## Capabilities

### New Capabilities

### Modified Capabilities
- `runtime-logging`: se añade el requisito de cuándo se registra la configuración al arrancar (solo desarrollo o con flag explícito, y siempre como log estructurado). Los requisitos existentes no cambian.

## Impact

- Código: `src/core/settings.py` (`print_settings`, nuevo campo `PRINT_SETTINGS`), `src/__init__.py` (llamada en `create_app`).
- Config: `.env.example`.
- Sin cambios de dependencias, API ni BD. En producción desaparece una línea del arranque en `docker logs`.
