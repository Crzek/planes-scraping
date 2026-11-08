# web-interface Specification

## Purpose
Define la apariencia y usabilidad de las páginas HTML que sirve la aplicación: una identidad visual común, formularios claros, una tabla de vuelos legible y un uso accesible tanto en escritorio como en móvil.

## Requirements

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
Al imprimir la página de una tabla de vuelos, la aplicación SHALL ajustar la tabla para que todas sus columnas visibles, la de matrículas y las de horas dentro del rango elegido, quepan en el ancho de una hoja A4 vertical sin recortar ninguna, y SHALL imprimirla un 2/3 más ancha que antes de este cambio (5/3 de su ancho impreso anterior), con letra y celdas proporcionalmente mayores, hasta un máximo igual al ancho útil de la hoja. No SHALL imprimir las columnas de horas ni las filas de matrículas ocultas por la configuración, la cabecera del sitio, el enlace "home", la barra de herramientas ni los controles de edición. Esto SHALL cumplirse en las tablas nuevas y en las guardadas antes del cambio.

#### Scenario: Tabla completa en una hoja
- **WHEN** el usuario con el rango por defecto imprime la tabla de un día en una hoja A4 vertical
- **THEN** salen la columna de matrículas y las 13 columnas de horas de 8 a 20, sin cortes por el lado derecho

#### Scenario: Tabla más grande al imprimir
- **WHEN** el usuario imprime una tabla cuyo ancho impreso anterior era A
- **THEN** la tabla impresa mide 5/3 de A, o el ancho útil de la hoja si 5/3 de A lo supera, y la letra de las celdas es mayor que la de 7 pt anterior

#### Scenario: Solo lo configurado
- **WHEN** el usuario tiene el rango de 10 a 16 h y una matrícula oculta e imprime la tabla
- **THEN** la hoja contiene las 7 columnas de horas de 10 a 16 y no incluye la fila de la matrícula oculta, con la tabla un 2/3 más ancha que antes sin pasar del ancho útil

#### Scenario: Solo el contenido útil
- **WHEN** el usuario abre la vista previa de impresión de la tabla
- **THEN** aparecen el título con la fecha y la tabla, y no la cabecera del sitio, el enlace "home", la barra de herramientas ni los botones de edición

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

### Requirement: La tabla tiene una barra de herramientas superior
La página de la tabla de vuelos SHALL mostrar encima de la tabla una barra de herramientas con el botón de habilitar/deshabilitar edición y, para usuarios con sesión, los accesos a Horas y Avionetas. La barra MUST estar visible sin desplazarse hasta el final de la tabla y MUST NOT insertarse dentro de ella. La tabla SHALL cargar con la edición deshabilitada, como hasta ahora.

#### Scenario: Botón de edición arriba
- **WHEN** el usuario abre la tabla de un día con muchas filas
- **THEN** el botón de habilitar edición está encima de la tabla, visible al cargar, y no hay ningún botón de edición al final

#### Scenario: Alternar la edición
- **WHEN** el usuario pulsa el botón de edición
- **THEN** aparecen los controles de fila y el botón pasa a ofrecer deshabilitar la edición

#### Scenario: Barra sin sesión
- **WHEN** un usuario sin sesión abre la tabla
- **THEN** la barra muestra el botón de edición pero no los accesos a Horas ni a Avionetas

#### Scenario: Barra en móvil
- **WHEN** se abre la tabla en una pantalla de 360 px de ancho
- **THEN** los botones de la barra caben o se reparten en varias líneas, sin desplazamiento horizontal de la página, y cada uno tiene al menos 44 px de alto

### Requirement: Los diálogos de la tabla son accesibles
El diálogo de matrículas y el aviso de horas con vuelos SHALL tener un título, poder usarse solo con teclado, devolver el foco al control que los abrió al cerrarse y cerrarse con Escape. Cada casilla MUST tener su matrícula como etiqueta visible.

#### Scenario: Uso con teclado
- **WHEN** el usuario abre el diálogo de matrículas con el teclado, recorre las casillas con Tab y las cambia con la barra espaciadora
- **THEN** cada casilla enseña un indicador de foco visible y cambia de estado

#### Scenario: Cierre y foco
- **WHEN** el usuario cierra un diálogo con Escape
- **THEN** el diálogo desaparece y el foco vuelve al botón que lo abrió
