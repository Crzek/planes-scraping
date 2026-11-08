# Tasks

## 1. CSS de impresión

- [x] 1.1 Medir el ancho impreso actual de la tabla con el rango por defecto (vista previa de impresión, A4 vertical) y anotarlo; verificar que la medida queda registrada en el commit o nota del PR
- [x] 1.2 En `@media print` de `src/auth/statics/styles/styles.css`, subir ~×5/3 la letra, `min-width`, `max-width` de matrículas y padding de `.dataframe`, manteniendo `max-width: 100%`; verificar en vista previa que la tabla ocupa 5/3 del ancho anterior o todo el ancho útil si no cabe
- [x] 1.3 Comprobar la tabla con rango por defecto (8–20), rango reducido (10–16 con una matrícula oculta) y rango completo (0–23): sin columnas recortadas, cabecera repetida y filas sin partir entre hojas

## 2. Verificación

- [x] 2.1 Imprimir a PDF una tabla nueva y una guardada antes del cambio (solo 8–20); verificar que ambas salen más grandes, completas y sin cabecera del sitio ni controles de edición
- [x] 2.2 Revisar la impresión en blanco y negro: las celdas con vuelo se distinguen y la hora se lee con la letra nueva
