# Spec Delta

## ADDED Requirements

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
