# Design

## Context

La impresión se define en el bloque `@media print` de `src/auth/statics/styles/styles.css` (tras `@page { size: A4 portrait; margin: 10mm }`, ancho útil 190 mm). La tabla usa `width: max-content; max-width: 100%`, letra de 7 pt, columnas de hora con `min-width: 9mm` y la de matrículas con `max-width: 17mm`. Con 13 columnas queda en torno a 134 mm: bastante menos que la hoja. Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- Ancho impreso ≈ 5/3 del actual, con tope en 190 mm.
- Letra y celdas crecen en proporción para que la tabla se lea más grande, no solo más separada.

**Non-Goals:**
- Cambiar orientación o tamaño de hoja, la vista en pantalla o el Excel.
- Escalar con `zoom`/`transform` (frágil entre navegadores).

## Decisions

- **Escalar con unidades del propio bloque `@media print`**: subir ×5/3 la letra (7 pt → ~11,5 pt), el `min-width` de hora (9 mm → ~15 mm), el `max-width` de la columna de matrículas (17 mm → ~28 mm) y el padding. Alternativa descartada: `width: 100%` fijo, que estira columnas sin agrandar la letra y no cumple "2/3 más".
- **Tope en el ancho útil**: se mantiene `max-width: 100%`. Con el rango por defecto 5/3 de 134 mm ≈ 223 mm supera 190 mm, así que la tabla llenará la hoja; en ese caso la letra se ajusta (≈ 9–10 pt) para que no haya recorte. Con menos columnas se aplica el ×5/3 completo.
- **Ajuste de letra por tope**: la letra y el ancho se definen de forma que 13 columnas + matrículas quepan en 190 mm; se valida en vista previa y se fija el valor final en la implementación.

## Risks / Trade-offs

- [Con el rango 0–23 (24 columnas) la letra mayor no cabe] → el tope de 190 mm manda y la letra se reduce o las columnas se estrechan; se comprueba en vista previa que no hay recorte.
- [Matrículas con "Private booking" ocupan más filas] → ya pasa a dos líneas; con letra mayor puede ser a tres: se acepta, las filas no se parten entre hojas.
- [Menos filas por hoja] → más hojas con la cabecera repetida; aceptado por legibilidad.
