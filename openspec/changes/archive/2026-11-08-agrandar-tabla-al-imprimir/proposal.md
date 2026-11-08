# Proposal

## Why

Al imprimir la tabla de vuelos (A4 vertical) el PDF sale pequeño: la tabla ocupa solo una parte del ancho de la hoja, con letra de 7 pt, y cuesta leerla. El cambio anterior (`configurar-tabla-vuelos`, archivado el 2026-11-08) priorizó que cupiera completa; ahora hay que aprovechar el ancho disponible.

## What Changes

- Al imprimir, la tabla de vuelos se hace un 2/3 más ancha que ahora (≈ ×1,67 su ancho impreso actual), con letra y celdas proporcionalmente más grandes.
- El ancho nunca supera el útil de la hoja A4 vertical (190 mm): si el aumento de 2/3 no cabe, la tabla ocupa todo el ancho útil. Sigue sin recortarse ninguna columna.
- Sin cambios en pantalla, en los datos, en la configuración de horas/matrículas ni en el Excel.

## Capabilities

### New Capabilities
<!-- ninguna -->

### Modified Capabilities
- `web-interface`: el requisito "La tabla de vuelos se imprime completa" pasa a exigir un tamaño impreso mayor (+2/3 de ancho, con tope en el ancho útil de la hoja).

## Impact

- `src/auth/statics/styles/styles.css`: bloque `@media print` (tamaños de letra, `min-width` y padding de celdas, ancho de la tabla).
- Sin cambios en Python, modelos, migraciones ni JS.

## Assumptions

- "2/3 más de ancho" se interpreta como multiplicar por 5/3 el ancho impreso actual, no como pasar a 2/3 del ancho de la hoja.
- Se mantiene A4 vertical; las filas largas seguirán paginando con la cabecera repetida.
