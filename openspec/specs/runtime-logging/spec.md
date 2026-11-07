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

### Requirement: La configuración solo se registra en desarrollo o con flag explícito
Al arrancar, la aplicación SHALL registrar la configuración cargada únicamente cuando `DEBUG` es verdadero o `PRINT_SETTINGS` es verdadero. En cualquier otro caso MUST NOT escribirla en su salida.

#### Scenario: Arranque en desarrollo
- **WHEN** la aplicación arranca con `DEBUG=True`
- **THEN** el log muestra la configuración cargada

#### Scenario: Arranque en producción sin flag
- **WHEN** la aplicación arranca con `DEBUG=False` y `PRINT_SETTINGS` sin definir
- **THEN** la salida de logs no contiene ninguna línea con la configuración (ni `FLASK_APP=`, ni `DATABASE_HOST=`, ni `user=`)

#### Scenario: Producción con diagnóstico activado
- **WHEN** la aplicación arranca con `DEBUG=False` y `PRINT_SETTINGS=true`
- **THEN** el log muestra la configuración cargada, con los secretos enmascarados

### Requirement: La configuración se registra como mensaje de log
Cuando la configuración se registra, la aplicación SHALL emitirla mediante el sistema de logging, de modo que cada línea lleve hora, nivel y origen como el resto de mensajes, y no como salida directa sin formato.

#### Scenario: Formato de la línea de configuración
- **WHEN** la configuración se registra al arrancar
- **THEN** la línea comienza con la marca de tiempo y el nivel, igual que `***** Inicio de la app *****`
