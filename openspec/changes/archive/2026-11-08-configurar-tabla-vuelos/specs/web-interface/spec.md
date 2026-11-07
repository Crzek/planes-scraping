# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: La tabla de vuelos se imprime completa
Al imprimir la página de una tabla de vuelos, la aplicación SHALL ajustar la tabla para que todas sus columnas visibles, la de matrículas y las de horas dentro del rango elegido, quepan en el ancho de una hoja A4 vertical sin recortar ninguna. No SHALL imprimir las columnas de horas ni las filas de matrículas ocultas por la configuración, la cabecera del sitio, el enlace "home", la barra de herramientas ni los controles de edición. Esto SHALL cumplirse en las tablas nuevas y en las guardadas antes del cambio.

#### Scenario: Tabla completa en una hoja
- **WHEN** el usuario con el rango por defecto imprime la tabla de un día en una hoja A4 vertical
- **THEN** salen la columna de matrículas y las 13 columnas de horas de 8 a 20, sin cortes por el lado derecho

#### Scenario: Solo lo configurado
- **WHEN** el usuario tiene el rango de 10 a 16 h y una matrícula oculta e imprime la tabla
- **THEN** la hoja contiene las 7 columnas de horas de 10 a 16 y no incluye la fila de la matrícula oculta

#### Scenario: Solo el contenido útil
- **WHEN** el usuario abre la vista previa de impresión de la tabla
- **THEN** aparecen el título con la fecha y la tabla, y no la cabecera del sitio, el enlace "home", la barra de herramientas ni los botones de edición

#### Scenario: Más filas que una hoja
- **WHEN** la tabla tiene más filas de las que caben en una hoja
- **THEN** continúa en la hoja siguiente con la fila de horas repetida arriba y ninguna fila queda partida entre dos hojas

#### Scenario: Impresión sin fondos
- **WHEN** el usuario imprime en blanco y negro o con los gráficos de fondo desactivados
- **THEN** las celdas con vuelo se siguen distinguiendo de las vacías, con borde y negrita, y la hora se lee
