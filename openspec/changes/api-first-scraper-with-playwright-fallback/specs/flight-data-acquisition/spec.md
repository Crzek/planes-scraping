# Spec Delta

## Purpose

Define cómo el sistema obtiene las reservas de vuelo de un día desde private-radar, usando la API como fuente primaria y el navegador automatizado como respaldo, de modo que el resultado sea equivalente con independencia de la fuente.

## ADDED Requirements

### Requirement: API como fuente primaria
El sistema SHALL intentar obtener las reservas del día solicitado (hoy o mañana) mediante la API de private-radar antes de recurrir a cualquier otra fuente.

#### Scenario: La API responde correctamente
- **WHEN** se solicita la generación de vuelos de un día y el login y la consulta de reservas por API tienen éxito
- **THEN** el sistema genera los datos de vuelos a partir de la respuesta de la API sin abrir ningún navegador

#### Scenario: Día solicitado
- **WHEN** el usuario pide "hoy" o "mañana"
- **THEN** la consulta a la API usa la fecha correspondiente a ese día

### Requirement: Fallback a navegador automatizado
El sistema SHALL recurrir al flujo de navegador automatizado (Playwright) cuando la ruta API no pueda producir datos válidos.

#### Scenario: Login rechazado o error de red
- **WHEN** el login por API devuelve un error de autenticación, un error HTTP, o expira el tiempo de espera
- **THEN** el sistema ejecuta el flujo Playwright y devuelve su resultado

#### Scenario: Respuesta con esquema inesperado
- **WHEN** la respuesta de reservas de la API no es JSON válido o carece de los campos necesarios (hora de salida, hora de llegada, matrícula, persona)
- **THEN** el sistema descarta la respuesta de la API y ejecuta el flujo Playwright

#### Scenario: Ambas fuentes fallan
- **WHEN** tanto la API como Playwright fallan
- **THEN** el sistema informa al usuario de un error al cargar los vuelos y no deja un archivo de vuelos parcial o desactualizado presentado como nuevo

### Requirement: Resultado equivalente entre fuentes
El sistema SHALL producir los mismos artefactos de salida (Excel, HTML y PDF de vuelos) con el mismo formato, sea cual sea la fuente utilizada.

#### Scenario: Mismas reglas de filtrado
- **WHEN** los datos provienen de la API
- **THEN** se aplican las mismas reglas que con Playwright: se excluyen los aviones de la lista de exclusión, las reservas canceladas, de mantenimiento, no disponibles y de tipo "type rating", y solo se incluyen reservas DUAL o PIC

#### Scenario: Reserva cancelada
- **WHEN** una reserva de la API tiene un motivo de cancelación no vacío
- **THEN** la reserva no aparece en los datos de vuelos generados

#### Scenario: Reserva sin motivo de cancelación
- **WHEN** una reserva de la API no tiene el campo de motivo de cancelación o este está vacío
- **THEN** la reserva se considera activa y se incluye si cumple el resto de reglas

#### Scenario: Mismo formato de horas
- **WHEN** se procesa una reserva obtenida por API cuyas horas llegan como marcas de tiempo en milisegundos
- **THEN** las horas de salida y llegada se convierten a hora local de Madrid y se representan con el formato `HH:MM` que ya consumen las tablas de salida por hora

### Requirement: Observabilidad de la fuente
El sistema MUST registrar en log qué fuente se utilizó en cada ejecución y, en caso de fallback, el motivo.

#### Scenario: Fallback registrado
- **WHEN** se produce un fallback de API a Playwright
- **THEN** el log indica la fuente final `playwright` y la causa del fallo de la API, sin incluir credenciales ni tokens

### Requirement: Protección de credenciales
El sistema MUST leer las credenciales de private-radar únicamente de la configuración de entorno, y MUST NOT escribir contraseñas ni tokens en logs, respuestas al usuario o archivos versionados.

#### Scenario: Token de sesión
- **WHEN** el login por API devuelve un token
- **THEN** el token se mantiene solo en memoria durante la ejecución y no se persiste ni se registra

### Requirement: Límites de ejecución de la API
El sistema SHALL aplicar un tiempo máximo a cada petición a la API y MUST NOT reintentar de forma indefinida.

#### Scenario: Tiempo de espera agotado
- **WHEN** una petición a la API supera el tiempo máximo configurado
- **THEN** se trata como fallo de la ruta API y se activa el fallback
