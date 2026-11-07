# Spec Delta

## Purpose

Define la apariencia y usabilidad de las páginas HTML que sirve la aplicación: una identidad visual común, formularios claros, una tabla de vuelos legible y un uso accesible tanto en escritorio como en móvil.

## ADDED Requirements

### Requirement: Todas las páginas comparten la misma identidad visual
Toda página HTML que sirve la aplicación (inicio, login, registro, agradecimiento, vuelos, tabla de vuelos, contenido genérico, error 404 y error 500) SHALL cargar la misma hoja de estilos propia y mostrar la misma cabecera, tipografía y paleta. Ninguna página MUST depender de una hoja de estilos alojada en un servidor externo.

#### Scenario: Páginas con aspecto coherente
- **WHEN** un usuario navega de login a registro, a vuelos y a una página de error
- **THEN** todas las páginas muestran la misma tipografía, los mismos colores y la misma cabecera

#### Scenario: Sin conexión a internet
- **WHEN** el navegador no tiene acceso a internet y carga cualquier página de la aplicación
- **THEN** la página se muestra con su estilo completo, sin peticiones a dominios externos

#### Scenario: Páginas que hoy no tienen estilo
- **WHEN** se abre la página de inicio del scraper o se provoca un error 500
- **THEN** la página usa el mismo estilo que el resto y no se ve como HTML sin formato

### Requirement: Las páginas declaran el idioma español
Cada página SHALL declarar `lang="es"` en su elemento raíz y MUST usar textos de interfaz en español, en minúsculas salvo la inicial (sentence case).

#### Scenario: Idioma del documento
- **WHEN** se carga cualquier página de la aplicación
- **THEN** el elemento `<html>` tiene `lang="es"`

### Requirement: Los formularios son claros y accesibles
Cada campo de los formularios de login, registro y generación de vuelos SHALL tener una etiqueta visible asociada a su control. Un error de validación SHALL mostrarse junto al campo afectado, con un texto que explique qué corregir. Cada control MUST mostrar un indicador de foco visible al navegar con teclado.

#### Scenario: Etiquetas asociadas
- **WHEN** un usuario hace clic en la etiqueta de un campo
- **THEN** el foco pasa a ese campo

#### Scenario: Error de login
- **WHEN** el usuario envía el login con un email o una contraseña erróneos
- **THEN** el mensaje de error aparece junto al campo afectado, distinguible por algo más que el color

#### Scenario: Navegación con teclado
- **WHEN** el usuario recorre el formulario con la tecla Tab
- **THEN** cada campo y botón enseña un contorno de foco claramente visible

### Requirement: La tabla de vuelos es legible de un vistazo
La tabla de vuelos SHALL mostrar las horas y las matrículas con una tipografía de cifras de ancho fijo, dejar vacías las celdas sin vuelo y mantener visibles la fila de horas y la columna de matrículas al desplazar la tabla. Esto SHALL aplicarse tanto a las tablas generadas después de este cambio como a los HTML ya guardados.

#### Scenario: Tabla recién generada
- **WHEN** el usuario abre la tabla de un día generado tras este cambio
- **THEN** las horas se alinean en columnas, las celdas sin vuelo están vacías y la tabla usa el estilo común

#### Scenario: Tabla guardada antes de este cambio
- **WHEN** el usuario abre un HTML de `static/html/` generado antes del cambio
- **THEN** la tabla se muestra con el mismo estilo común y sin los bordes negros anteriores

#### Scenario: Tabla más ancha que la pantalla
- **WHEN** la tabla no cabe en el ancho de la pantalla y el usuario la desplaza en horizontal
- **THEN** la columna de matrículas sigue visible y solo la tabla se desplaza, no la página entera

### Requirement: Las líneas de la cuadrícula se distinguen con claridad
La tabla de vuelos SHALL separar cada fila de la siguiente con una línea continua más marcada que las líneas verticales, para seguir una matrícula hasta la hora de su vuelo sin perder la fila. Esa línea MUST contrastar al menos 3:1 con el fondo de la tabla y MUST seguir viéndose al imprimir en blanco y negro.

#### Scenario: Lectura en pantalla
- **WHEN** el usuario abre la tabla de un día
- **THEN** cada fila queda separada de la siguiente por una línea horizontal claramente visible, más marcada que las líneas verticales

#### Scenario: Lectura en papel
- **WHEN** el usuario imprime la tabla en blanco y negro
- **THEN** las líneas entre filas salen oscuras y continuas, y permiten seguir la fila de una matrícula hasta la hora de su vuelo

### Requirement: La tabla de vuelos se imprime completa
Al imprimir la página de una tabla de vuelos, la aplicación SHALL ajustar la tabla para que todas sus columnas, la de matrículas y todas las de horas, quepan en el ancho de una hoja A4 vertical sin recortar ninguna. No SHALL imprimir la cabecera del sitio, el enlace "home" ni los controles de edición. Esto SHALL cumplirse en las tablas nuevas y en las guardadas antes del cambio.

#### Scenario: Tabla completa en una hoja
- **WHEN** el usuario imprime la tabla de un día con horas de 8 a 20 en una hoja A4 vertical
- **THEN** salen la columna de matrículas y las 13 columnas de horas, sin cortes por el lado derecho

#### Scenario: Solo el contenido útil
- **WHEN** el usuario abre la vista previa de impresión de la tabla
- **THEN** aparecen el título con la fecha y la tabla, y no la cabecera del sitio, el enlace "home" ni los botones de edición

#### Scenario: Más filas que una hoja
- **WHEN** la tabla tiene más filas de las que caben en una hoja
- **THEN** continúa en la hoja siguiente con la fila de horas repetida arriba y ninguna fila queda partida entre dos hojas

#### Scenario: Impresión sin fondos
- **WHEN** el usuario imprime en blanco y negro o con los gráficos de fondo desactivados
- **THEN** las celdas con vuelo se siguen distinguiendo de las vacías, con borde y negrita, y la hora se lee

### Requirement: La edición de la tabla conserva su funcionamiento
Los controles que permiten añadir una fila debajo y eliminar una fila SHALL seguir funcionando y SHALL mostrarse con el estilo de botón común, con nombres de acción que describan lo que hacen.

#### Scenario: Añadir fila
- **WHEN** el usuario pulsa el control de añadir fila en una fila de la tabla
- **THEN** aparece una fila vacía justo debajo, con el mismo estilo que las demás

#### Scenario: Eliminar fila
- **WHEN** el usuario pulsa el control de eliminar fila
- **THEN** esa fila desaparece de la tabla

### Requirement: El estado de generación de vuelos es visible
Al enviar el formulario de generar vuelos, la página SHALL ocultar el formulario y mostrar un indicador de carga con un texto que diga que se están extrayendo los datos y que puede tardar. El indicador MUST anunciarse a los lectores de pantalla como estado y MUST NOT animarse si el usuario pidió reducir el movimiento.

#### Scenario: Envío del formulario
- **WHEN** el usuario envía el formulario de generar vuelos
- **THEN** el formulario se oculta y aparece el indicador de carga con su mensaje

#### Scenario: Movimiento reducido
- **WHEN** el sistema del usuario tiene activada la preferencia de movimiento reducido
- **THEN** el indicador de carga se muestra sin animación

### Requirement: Las páginas funcionan en móvil
Toda página SHALL ser utilizable con un ancho de 360 px sin desplazamiento horizontal de la página. Los botones y enlaces principales MUST tener un área táctil de al menos 44 px de alto.

#### Scenario: Login en móvil
- **WHEN** se abre el login en una pantalla de 360 px de ancho
- **THEN** el formulario ocupa el ancho disponible y la página no se desplaza en horizontal

#### Scenario: Página de vuelos con resultados
- **WHEN** se abre la página de vuelos de un día ya generado en 360 px de ancho
- **THEN** los enlaces de descarga y de la tabla se leen completos y se pueden tocar con facilidad

### Requirement: Los colores cumplen el contraste mínimo
El texto y los controles SHALL tener un contraste mínimo de 4,5:1 (3:1 para texto grande y bordes de controles) frente a su fondo. La información MUST NOT depender solo del color.

#### Scenario: Texto sobre fondo
- **WHEN** se mide el contraste del texto de cuerpo, de los enlaces y de los botones frente a su fondo
- **THEN** ninguno queda por debajo de 4,5:1

### Requirement: El rediseño no cambia el comportamiento de la aplicación
El rediseño MUST NOT cambiar las rutas, los nombres de los campos de formulario ni los datos que envían los formularios. Todas las acciones disponibles antes del cambio (iniciar sesión, registrarse, cerrar sesión, generar vuelos, descargar el Excel, abrir la tabla) SHALL seguir disponibles.

#### Scenario: Flujo completo
- **WHEN** un usuario inicia sesión, genera los vuelos de hoy, descarga el Excel y abre la tabla
- **THEN** cada paso funciona igual que antes del cambio
