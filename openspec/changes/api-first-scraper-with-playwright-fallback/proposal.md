# Proposal

## Why

El scraper actual (Playwright, `src/app/automation/main_scraper.py`) depende de selectores CSS/XPath absolutos del front de private-radar (p. ej. `/html/body/div[4]/div[3]/...`) y de esperas fijas (`wait_for_timeout` de hasta 20 s). Cada vez que la web cambia hay que volver a inspeccionarla y reparar los selectores, y es lento y frágil. Inspeccionando el Network se han identificado los endpoints JSON que usa el propio front (login y listado de reservas), que son un contrato mucho más estable y rápido que el DOM.

## What Changes

- Añadir un cliente HTTP para la API de private-radar: login (`POST https://api4.private-radar.com/auth/user/login`) y consulta de reservas del día (`POST https://acbs.private-radar.com/prwsw/bookings/getByFilterNew`), autenticado con el token devuelto por el login.
- Adaptar la respuesta JSON al mismo formato interno que hoy alimenta `AirCraft`/`Book` y `clas_to_series` (hora de salida, hora de llegada, matrícula, persona), manteniendo las mismas reglas de filtrado (solo reservas DUAL/PIC, exclusión de `No_Plane`, tipos de reserva excluidos).
- Nuevo orquestador "API primero": intenta la ruta API y, si falla (login rechazado, error HTTP/red, timeout, respuesta con esquema inesperado o sin datos válidos), recurre automáticamente al flujo Playwright existente.
- Registrar en log qué fuente se usó (`api` o `playwright`) y el motivo del fallback.
- Credenciales y URLs de la API solo por configuración (`.env` / `Settings`); nunca en código ni en artefactos.
- Primera fase: **estudio de viabilidad** (ejecutar las dos peticiones y verificar que la respuesta contiene todos los campos necesarios). Si no es viable, el cambio se detiene sin tocar el flujo actual.
- Playwright **no se elimina** en este cambio; queda como fallback. Su retirada, si procede, será un cambio posterior.

## Capabilities

### New Capabilities
- `flight-data-acquisition`: obtención de las reservas de vuelo de un día (hoy/mañana) desde private-radar, con la API como fuente primaria y Playwright como fallback, devolviendo un resultado equivalente en ambos casos.

### Modified Capabilities
<!-- Ninguna: no existen specs previas en openspec/specs/. -->

## Impact

- **Código**: `src/app/automation/main_scraper.py` (se reutiliza como fallback; el punto de entrada cambia), nuevo módulo de cliente API en `src/app/` (ubicación a fijar en design), `src/auth/routes.py` (la ruta que invoca `main_scraper` pasa a llamar al orquestador), `src/app/utils/utils.py` (reutilización de `save_Book_by_tag`/`clas_to_series`; sin cambios de comportamiento previstos).
- **Configuración**: `src/core/settings.py` y `.env.example` (URLs de API; reutiliza `user`/`password` existentes).
- **Dependencias**: cliente HTTP (`requests` o `httpx`; a decidir en design; hoy no hay ninguno como dependencia directa).
- **Sistemas externos**: API no documentada ni pública de private-radar; puede cambiar o aplicar límites sin aviso (riesgo mitigado por el fallback).
- **Seguridad**: las credenciales y el token de ejemplo se pegaron en el chat al preparar este cambio; se recomienda rotar la contraseña de esa cuenta y no versionar ningún `curl` con credenciales.
- **Sin impacto** en BD, migraciones, Excel/HTML/PDF generados ni en el frontend.
