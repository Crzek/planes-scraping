# runtime-logging Specification

## Purpose
Define qué registra la aplicación en su salida de logs al ejecutarse y qué datos sensibles nunca deben aparecer en ella.

## Requirements

### Requirement: Los mensajes INFO de la aplicación se ven en los logs
La aplicación SHALL emitir sus mensajes de nivel INFO o superior por la salida de error estándar desde que arranca, también cuando se ejecuta con gunicorn dentro de Docker.

#### Scenario: Arranque de la app
- **WHEN** se arranca la aplicación con `docker compose up`
- **THEN** `docker logs` muestra la línea `***** Inicio de la app *****`

#### Scenario: Fuente de vuelos visible
- **WHEN** se generan vuelos desde la web
- **THEN** el log muestra `fuente de vuelos: api` o `fuente de vuelos: playwright`, según la fuente usada

### Requirement: La contraseña de la base de datos no aparece en los logs
La aplicación MUST NOT escribir el valor de `DATABASE_PASS` en su salida, ni al imprimir la configuración al arrancar ni en la URI de la base de datos que registra. La conexión a la base de datos SHALL seguir usando el valor real.

#### Scenario: Impresión de la configuración al arrancar
- **WHEN** la aplicación arranca con `DATABASE_PASS` definida
- **THEN** la configuración impresa muestra `DATABASE_PASS` enmascarado y no contiene su valor

#### Scenario: Conexión a la base de datos
- **WHEN** la aplicación se conecta a PostgreSQL con `DATABASE_PASS` definida
- **THEN** la conexión usa la contraseña real y el log muestra `DB connection: OK`
