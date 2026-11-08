# Spec Delta

## MODIFIED Requirements

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
