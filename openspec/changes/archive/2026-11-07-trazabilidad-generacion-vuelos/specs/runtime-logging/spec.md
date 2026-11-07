## ADDED Requirements

### Requirement: Cada generación de vuelos lleva un identificador de petición
La aplicación SHALL asignar a cada generación de vuelos un identificador corto y emitirlo en todas las líneas de log de esa generación, de modo que las líneas de peticiones simultáneas puedan separarse. El identificador SHALL aparecer también en las líneas emitidas durante el respaldo con navegador automatizado.

#### Scenario: Dos peticiones simultáneas
- **WHEN** dos usuarios piden generar vuelos al mismo tiempo en workers distintos
- **THEN** cada línea de log de la generación lleva el identificador de su petición y los dos identificadores son distintos

#### Scenario: Línea del navegador automatizado
- **WHEN** la API falla y la generación continúa con el navegador automatizado
- **THEN** las líneas de log de esa etapa llevan el mismo identificador que las anteriores de la misma petición

#### Scenario: Líneas fuera de una petición
- **WHEN** la aplicación registra un mensaje fuera de una generación de vuelos, como el de arranque
- **THEN** la línea se emite con normalidad, sin identificador de petición

### Requirement: El inicio y el final de la generación quedan registrados
La aplicación SHALL registrar una línea al comenzar cada petición de generación de vuelos, con el día solicitado, si se pidió seleccionar todos los tipos de reserva y si se reutiliza el Excel existente o se regenera. SHALL registrar otra línea al terminar con el resultado, la fuente usada y la duración total.

#### Scenario: Excel ya existente
- **WHEN** el usuario pide los vuelos de un día cuyo Excel ya existe y no solicita regenerarlo
- **THEN** el log indica que se reutiliza el Excel existente y no se consulta ninguna fuente

#### Scenario: Generación correcta
- **WHEN** la generación termina con éxito
- **THEN** la última línea de la petición indica la fuente (`api` o `playwright`), el número de reservas y la duración total en segundos

#### Scenario: Generación fallida
- **WHEN** ninguna fuente puede producir los vuelos
- **THEN** la última línea de la petición indica el fallo y la duración total hasta que se produjo

### Requirement: Las fases de la generación registran su duración
La aplicación SHALL registrar, al terminar cada fase de una generación de vuelos, el nombre de la fase y el tiempo que tardó. Las fases son: login en la API, consulta de reservas, parseo, guardado de reservas, generación de la tabla y aplicación de estilos al Excel. En el respaldo con navegador automatizado SHALL registrarse además la duración de cada etapa: login, apertura del calendario, configuración de filtros y lectura de reservas.

#### Scenario: Seguimiento de una generación por API
- **WHEN** una generación de vuelos se completa por la API
- **THEN** el log contiene, en orden, una línea por fase con su duración, todas con el mismo identificador de petición

#### Scenario: Seguimiento del respaldo
- **WHEN** la generación recurre al navegador automatizado
- **THEN** el log contiene una línea por etapa del navegador con su duración, además de la causa del fallo de la API

#### Scenario: Fase en curso al detenerse el worker
- **WHEN** un worker termina por superar el límite de tiempo de gunicorn durante una generación
- **THEN** la última línea de esa petición en el log identifica la fase que estaba en curso

### Requirement: El paso al respaldo avisa del tiempo disponible
Cuando la generación pasa de la API al navegador automatizado, la aplicación SHALL registrar un aviso con el motivo del fallo de la API y el límite de tiempo de petición configurado, para que una terminación del worker por límite de tiempo pueda reconocerse a partir de los logs.

#### Scenario: Fallo de la API
- **WHEN** la API falla y comienza el respaldo con navegador automatizado
- **THEN** el log muestra un aviso con el motivo del fallo y el límite de tiempo de petición

### Requirement: Los errores de generación se registran con traza
Cuando la generación de vuelos falla con una excepción, la aplicación SHALL registrar el error con su traza completa y el identificador de petición. El usuario SHALL seguir viendo el mensaje de error de la página sin la traza.

#### Scenario: Excepción durante la generación
- **WHEN** se produce una excepción no controlada durante la generación de vuelos
- **THEN** el log contiene el mensaje de error y la traza, y la página muestra solo el mensaje de error

### Requirement: Los logs de la generación no contienen datos sensibles ni ruido
Los mensajes de log de la generación de vuelos MUST NOT incluir credenciales, tokens de sesión ni el contenido de las reservas (tripulación, matrículas), y MUST NOT volcar HTML de la página. Tampoco SHALL registrarse rutas internas de ficheros que no ayuden a diagnosticar el proceso.

#### Scenario: Generación completa por cualquier fuente
- **WHEN** se genera un día de vuelos por la API o por el navegador automatizado
- **THEN** ninguna línea de log contiene la contraseña de private-radar, el token de la API, nombres de personas, ni fragmentos de HTML
