# flight-table-preferences Specification

## Purpose
Permite que cada usuario elija qué horas y qué avionetas ve en la tabla de vuelos y que esa elección se conserve en la base de datos entre sesiones y entre días.

## Requirements

### Requirement: El usuario elige el rango de horas visible
La tabla de vuelos SHALL ofrecer una hora inicial y una hora final (enteros de 0 a 23, con inicial menor o igual que final) y SHALL mostrar solo las columnas de hora dentro de ese rango, ambas incluidas. Sin preferencia guardada, el rango SHALL ser el actual, de 8 a 20 h.

#### Scenario: Rango por defecto
- **WHEN** un usuario sin preferencias abre la tabla de un día
- **THEN** ve las columnas de 8 a 20 h, como antes del cambio

#### Scenario: Ampliar el rango
- **WHEN** el usuario fija la hora inicial en 6 y la final en 22 sobre una tabla generada después de este cambio
- **THEN** la tabla muestra las columnas de 6 a 22 h

#### Scenario: Rango inválido
- **WHEN** el usuario fija una hora inicial mayor que la final
- **THEN** la aplicación rechaza el cambio, explica el motivo junto al campo y conserva el rango anterior

#### Scenario: Tabla guardada antes del cambio
- **WHEN** el usuario abre un HTML generado antes del cambio, que solo contiene las horas 8 a 20
- **THEN** las horas fuera de 8–20 no se ofrecen en los selectores y el rango efectivo se limita a las horas que la tabla contiene

### Requirement: Se avisa antes de ocultar horas con vuelos
Si el nuevo rango deja fuera alguna hora que tiene al menos un vuelo en la tabla abierta, la aplicación SHALL pedir confirmación antes de aplicarlo, indicando si los vuelos son anteriores a la hora inicial, posteriores a la final o ambos. Al cancelar, el rango MUST quedar como estaba y no se guarda nada.

#### Scenario: Vuelos previos a la hora inicial
- **WHEN** hay un vuelo a las 8:00 y el usuario fija la hora inicial en 10
- **THEN** aparece un aviso de que hay vuelos previos con las opciones Aceptar y Cancelar

#### Scenario: Vuelos posteriores a la hora final
- **WHEN** hay un vuelo a las 18:00 y el usuario fija la hora final en 16
- **THEN** aparece un aviso de que hay vuelos posteriores con las opciones Aceptar y Cancelar

#### Scenario: Aceptar el aviso
- **WHEN** el usuario pulsa Aceptar en el aviso
- **THEN** el rango se aplica a la tabla y se guarda

#### Scenario: Cancelar el aviso
- **WHEN** el usuario pulsa Cancelar en el aviso
- **THEN** la tabla mantiene el rango anterior y los selectores recuperan los valores anteriores

#### Scenario: Sin vuelos fuera del rango
- **WHEN** el nuevo rango solo deja fuera horas sin vuelos
- **THEN** el rango se aplica y se guarda sin pedir confirmación

### Requirement: El usuario elige qué matrículas se muestran
La aplicación SHALL ofrecer un diálogo que liste todas las matrículas de la tabla abierta, cada una con una casilla marcada si se muestra. Las matrículas desmarcadas SHALL ocultarse de la tabla. Una matrícula que aparezca por primera vez y no esté entre las ocultas SHALL mostrarse.

#### Scenario: Abrir el diálogo
- **WHEN** el usuario pulsa Avionetas
- **THEN** aparece un diálogo con todas las matrículas de la tabla, incluidas las ocultas, y cada casilla refleja si se muestra

#### Scenario: Ocultar una matrícula
- **WHEN** el usuario desmarca una matrícula y confirma el diálogo
- **THEN** la fila de esa matrícula desaparece de la tabla y el cambio se guarda

#### Scenario: Cerrar sin confirmar
- **WHEN** el usuario cierra el diálogo con Cancelar o con la tecla Escape
- **THEN** la tabla y las preferencias guardadas no cambian

#### Scenario: Ninguna matrícula marcada
- **WHEN** el usuario desmarca todas las matrículas
- **THEN** el diálogo no permite confirmar e indica que debe quedar al menos una

#### Scenario: Matrícula nueva
- **WHEN** la tabla de un día contiene una matrícula que el usuario nunca ha visto ni ocultado
- **THEN** la fila se muestra

### Requirement: Las preferencias se guardan por usuario en la base de datos
La aplicación SHALL guardar en la base de datos las preferencias de cada usuario autenticado (hora inicial, hora final y matrículas ocultas) y SHALL aplicarlas al abrir la tabla de cualquier día, en cualquier navegador y tras reiniciar el servidor. Las preferencias de un usuario MUST NOT afectar a las de otro.

#### Scenario: Persistencia entre sesiones
- **WHEN** el usuario cambia su rango, cierra sesión, inicia sesión desde otro navegador y abre la tabla
- **THEN** la tabla aparece con el rango que había guardado

#### Scenario: Persistencia entre días
- **WHEN** el usuario oculta una matrícula en la tabla de hoy y abre la tabla de mañana
- **THEN** esa matrícula también está oculta en la de mañana

#### Scenario: Usuarios independientes
- **WHEN** dos usuarios guardan rangos distintos
- **THEN** cada uno ve la tabla con su propio rango

#### Scenario: Fallo al guardar
- **WHEN** el guardado falla por un error del servidor o de la base de datos
- **THEN** la aplicación muestra un mensaje de error, mantiene la configuración anterior y no deja la tabla en un estado distinto al guardado

### Requirement: Solo los usuarios autenticados configuran la tabla
Los controles de Horas y Avionetas SHALL mostrarse solo a usuarios con sesión iniciada. Quien abra la tabla sin sesión SHALL verla con el rango por defecto y sin matrículas ocultas, y la aplicación MUST rechazar cualquier intento de leer o guardar preferencias sin sesión.

#### Scenario: Sin sesión
- **WHEN** alguien abre la tabla sin haber iniciado sesión
- **THEN** ve el rango por defecto, todas las matrículas y ningún control de Horas ni de Avionetas

#### Scenario: Guardado sin sesión
- **WHEN** se envía un cambio de preferencias sin sesión iniciada
- **THEN** la aplicación lo rechaza y no guarda nada
