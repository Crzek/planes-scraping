# Design

## Context

Estado actual (observado en el código):

- `src/auth/routes.py` (ruta de vuelos) llama a `asyncio.run(main_scraper(...))` y luego a `main_styles(...)`. `main_scraper` devuelve `(title_day, html_table)`; la ruta ignora `title_day` en la práctica.
- `main_scraper` hace login por formulario, navega al calendario, configura filtros por XPath, extrae el atributo `title` de cada `.react-draggable` y lo pasa a `save_Book_by_tag`, que lo trocea por `\n` (`hora`, `matrícula`, `persona`, …) y solo guarda las reservas cuyo texto contiene `DUAL` o `PIC`.
- El estado se acumula en el atributo de clase `AirCraft.all_reservas` (global). `clas_to_series` lo convierte en DataFrame, escribe el Excel y devuelve la tabla HTML.
- Hay `user`/`password`/`base_url` en `Settings` (`src/core/settings.py`).

Peticiones capturadas en DevTools (las dos únicas conocidas):

- Login: `POST api4.private-radar.com/auth/user/login`, JSON `{email, password}`. Verificado (2026-11-05): responde 200 con JSON `{token, expiresAt, refreshToken, refreshTokenExpiresAt, status, message}` y no establece cookies. El token (JWT) se envía en la cabecera `Authorization` sin prefijo `Bearer`. La consulta de reservas funciona solo con esa cabecera (sin cookie `refresh_token`) y con un `User-Agent` propio, y respondió 200 para los días 20261105 y 20261106.
- Reservas: `POST acbs.private-radar.com/prwsw/bookings/getByFilterNew`, JSON con filtros (`bookingTypes`, `strDate` en `YYYYMMDD`, `period: "D"`, …). **La forma de la respuesta no se ha visto.**

Ver `proposal.md` (Why) para la motivación.

Respuesta de reservas (verificada con `data.json`, muestra del 2026-11-05): objeto con `aircraftsWithBookings[]` (un elemento por avión, cada uno con su lista `bookings[]`). Campos que el adaptador usa:

| Dato | Campo | Notas observadas |
|---|---|---|
| Matrícula | `registration` | también existe a nivel de avión |
| Salida / llegada | `timestamp_begin`, `timestamp_end` | epoch en milisegundos; se convierten a `Europe/Madrid` y se formatean `HH:MM` |
| Cancelada | `cancel_reason` | ausente en 29/47 reservas; no vacío ⇒ cancelada (coincide con `curStatus == 2`); vacío o ausente ⇒ no cancelada |
| Persona | `crew[].firstname`, `crew[].lastname` | 1 o 2 tripulantes; `crew[].func` observados: `DUAL`, `PIC`, `SUPER`, `PICUS`, `PIC2`, `SPIC` |

El resto de campos de la respuesta (`usersLightWithBookings`, `curStatus`, `flight_type`, etc.) no se usan en este cambio.

## Goals / Non-Goals

**Goals:**
- Obtener las reservas del día por API con el mismo resultado final que el flujo Playwright.
- Fallback automático y transparente a Playwright.
- Cambio mínimo en el código existente de parseo/exportación.

**Non-Goals:**
- Eliminar Playwright o los selectores actuales.
- Cambiar modelos, BD, formato de Excel/HTML/PDF o frontend.
- Documentar o consumir otros endpoints de private-radar.
- Cachear tokens entre ejecuciones.

## Decisions

1. **Viabilidad primero (spike).** Antes de integrar, ejecutar las dos peticiones con un script desechable fuera del flujo de producción y guardar una respuesta de ejemplo **sin datos personales** como fixture. Si la respuesta no trae hora de salida/llegada, matrícula y persona, el cambio se detiene. *Alternativa:* integrar directamente y descubrir el esquema después → descartada, riesgo de trabajo inútil.

1b. **Cancelación por `cancel_reason`.** Una reserva se descarta si `cancel_reason` existe y no está vacío; no se usa `curStatus` porque su significado no está documentado. El payload sigue enviando todos los `bookingTypes` y el filtrado se hace en el adaptador (así no depende de cómo trate el servidor cada tipo).

1c. **Filtro DUAL/PIC.** Hoy se hace con `"DUAL" in info or "PIC" in info` sobre el texto del `title`, es decir, por subcadena. Con la API se aplica por subcadena sobre `crew[].func` para ser equivalente: así `PIC2`, `SPIC` y `PICUS` pasan el filtro. Con coincidencia exacta (`DUAL`/`PIC`) se perderían 4 de las 38 reservas activas del 2026-11-06 (las `PIC2`). Si el Excel de Playwright de ese día confirma que esas reservas aparecen, se mantiene la subcadena; si no, se pasa a coincidencia exacta (tarea 1.3).

2. **Módulo nuevo `src/app/api/` con cliente + adaptador.** El cliente (login + consulta) y el adaptador (JSON → registros normalizados `{takeoff, landing, plane, person, type}`) viven separados del scraper Playwright. *Alternativa:* añadirlo a `main_scraper.py` → descartada para no mezclar dos estrategias y poder borrar Playwright más tarde.

3. **Alimentar el pipeline existente en un punto común.** Extraer de `save_Book_by_tag` la parte que crea `AirCraft`/`Book` (`takeoff, landing, persona, plane`) a una función reutilizable; `save_Book_by_tag` sigue parseando el texto y la delega. El adaptador de la API llama a la misma función. *Alternativa:* fabricar strings `title` falsos para reutilizar `save_Book_by_tag` → descartada por frágil. Regla DUAL/PIC y `No_Plane` se mantienen en un único sitio.

4. **Orquestador síncrono `get_flights(...)`** que intenta API y, ante cualquier fallo definido en la spec, limpia el estado acumulado (`AirCraft.all_reservas`) y ejecuta `asyncio.run(main_scraper(...))`. Mantiene la misma firma de retorno que `main_scraper` para que la ruta cambie solo la llamada. La limpieza evita mezclar datos parciales de la API con los de Playwright.

5. **Cliente HTTP: `requests`** (síncrono, simple, la ruta ya es síncrona). Timeout explícito (p. ej. 10 s) por petición, sin reintentos infinitos (máx. 1 reintento en errores de red). *Alternativa:* `httpx` → válida, sin ventaja clara aquí.

6. **Configuración.** Nuevas variables en `Settings`/`.env.example`: URL base de la API de login y de reservas, y un interruptor `USE_API_FIRST` (por defecto activo) para poder forzar Playwright sin redeploy. Se reutilizan `user`/`password`.

7. **Cabeceras.** Enviar `Content-Type`, `Accept` y `Referer`; no suplantar un `User-Agent` de navegador concreto: usar uno identificable genérico. Si el servidor lo rechaza, se decide en el spike.

7b. **Verificación TLS con intermedio incluido.** `api4.private-radar.com` no envía el certificado intermedio (`Sectigo Public Server Authentication CA DV R36`), por lo que `requests`, `curl` y `openssl` fallan con `unable to get local issuer certificate` (los navegadores lo completan por AIA). Decisión: versionar el intermedio en `certs/sectigo-dv-r36.pem` (público, verificado contra la raíz Sectigo R46, válido hasta 2036) y pasar a `requests` un bundle con `certifi` + ese intermedio. *Alternativa:* `verify=False` → descartada, envía la contraseña sin verificar el servidor. `acbs.private-radar.com` envía la cadena completa y no lo necesita. Debe copiarse a la imagen Docker.

8. **Logging seguro.** Registrar fuente, código HTTP y motivo; nunca cuerpo de login, contraseña ni token.

## Risks / Trade-offs

- **API privada sin contrato** → puede cambiar o aplicar límites/bloqueos sin aviso. Mitigación: validación estricta del esquema + fallback a Playwright + interruptor.
- **Esquema de respuesta desconocido** → puede no incluir todo lo necesario o requerir mapear códigos (tipos de reserva, estados). Mitigación: spike como paso 1 y decisión go/no-go.
- **Los filtros de tipo de reserva** (cancelada, mantenimiento, no disponible, type rating) hoy se aplican en la UI; por API hay que aplicarlos en el payload o en el adaptador. Mitigación: tests de equivalencia con fixtures.
- **Estado global `AirCraft.all_reservas`** → riesgo de mezclar ejecuciones. Mitigación: limpieza explícita antes de cada intento (ya es un problema latente en el flujo actual).
- **Términos de uso de private-radar** → consumir su API directamente no está confirmado como permitido. Mitigación: verificar con el propietario de la cuenta antes de activar por defecto (ver Open Questions).
- **Credenciales expuestas en el chat** (contraseña y token) → la contraseña no se puede rotar (la cuenta no la gestiona el usuario); tratar el token como caducado y no versionar credenciales.
- **Cadena TLS incompleta en `api4`** → si private-radar la corrige, el intermedio versionado sobra pero no estorba; si caduca (2036) o cambian de emisor, la ruta API falla y se activa el fallback. Mitigación: el fallo se registra como motivo de fallback.
- **Dos rutas que mantener** → coste de mantenimiento mientras Playwright siga como fallback; aceptable hasta decidir su retirada.

## Migration Plan

1. Desplegar con `USE_API_FIRST=false` (comportamiento idéntico al actual).
2. Activar en local/dev y comparar Excel de API vs Playwright para el mismo día.
3. Activar en producción (Raspberry Pi vía GitHub Actions) cuando coincidan.
4. Rollback: poner `USE_API_FIRST=false`; no hay migraciones de BD.

## Open Questions

- ¿Está permitido por los términos de private-radar el acceso directo a su API con esta cuenta? (no cambia el diseño, sí el momento de activarlo por defecto)
- ¿Cuánto dura el token (`expiresAt`)? El diseño hace login en cada ejecución y no lo cachea, así que no bloquea nada.
- ¿Qué significan exactamente los tipos de reserva nuevos (p. ej. `trip`) y los roles `PIC2`/`SPIC` respecto a lo que muestra hoy la UI? Se resuelve comparando con el Excel de Playwright (tarea 1.3).

## Comparación API vs Playwright (tarea 1.3, 2026-11-07)

Ejecutado en Docker local (imagen raíz) para 2026-11-07 y 2026-11-08, mismo día y misma cuenta, con `get_flights` en tres modos. Tiempos: API ~2 s, Playwright ~42 s.

| Modo | 07-11 aviones / reservas | 08-11 aviones / reservas | Log |
|---|---|---|---|
| API (`USE_API_FIRST=true`) | 21 / 48 | 17 / 47 | `fuente de vuelos: api` |
| Playwright (`USE_API_FIRST=false`) | 20 / 111 | 17 / 100 | `fuente de vuelos: playwright` |
| Fallback (login URL inválida) | igual que Playwright | igual que Playwright | `api fallo (login: http_404); fallback a playwright` |

Diferencias en la tabla final y su explicación (todas explicadas):

| Diferencia | Causa | ¿Cuál es correcta? |
|---|---|---|
| Playwright añade horas 20 min antes de la reserva (08:40 junto a 09:00, 11:40 junto a 12:00…) y duplica reservas | El `title` de Playwright incluye también el bloque con `prebrief_min`/`postbrief_min` (20/20): 08:40–10:50 frente a 09:00–10:30 | API: la hora de la reserva **no** incluye el prebriefing |
| Columna con otra hora (p. ej. EC-ERV 08-11: Playwright 15:40, API 15:00) | Efecto del punto anterior: la hora de prebriefing de la reserva siguiente (16:00 − 20 min) ocupa la columna de las 15h | API |
| Reservas `PIC2` (vuelos solo de alumno, p. ej. EC-JSN) solo en la API | Playwright no las extrae del `title`; el adaptador acepta `PIC2` porque contiene `PIC` | Decisión del usuario (pendiente) |
| `Private booking` en Playwright = `EC-MZF` en la API (mismas horas) | Reserva con `isprivate=true`: la UI oculta la matrícula; la API la da. EC-MZF es un velero GROB G103, base LECD | Decisión del usuario (pendiente): matrícula real o `Private booking` |
| Reservas canceladas (`cancel_reason` no vacío, p. ej. `Student no-show`) | Ninguna fuente las muestra | Igual |
| Nombres | API: `firstname lastname` completos; Playwright: nombre recortado con `[` final | API |

Respuesta a la Open Question de `PIC2`/`SPIC`: `PIC2` aparece como rol de vuelos `solo` y hoy Playwright no los muestra.
