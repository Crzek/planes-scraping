# Design

## Context

Estado actual (ver proposal.md para la motivación):

- Todas las plantillas Jinja salvo `index.html` y `page_500.html` extienden `base.html`, que carga Tailwind 2.2.19 por CDN. `base_clean.html` no carga ningún CSS y solo envuelve el HTML de la tabla con `{{ content|safe }}`.
- `src/auth/statics/styles/styles.css` está vacío. Los estáticos del blueprint se sirven con `url_for('authBP.static', ...)`.
- La tabla de vuelos es un `DataFrame.to_html()` con clase `dataframe`. Cada fichero guardado en `static/html/` lleva un `<style>` en línea con selectores de elemento (`table`, `th, td`) y un enlace `home`. `table.js` localiza la tabla con `.dataframe`, añade una primera celda de controles (`.control-buttons`) a cada fila y no debe romperse.
- `vuelos.js` depende de los ids `vuelosForm`, `remakeForm`, `loading` y `container-form`, y de la clase `hidden` para mostrar y ocultar.
- Los usuarios son personal del aeropuerto de Sabadell que consulta horarios de vuelos de escuela y aeroclub: matrículas (EC-ERV, EC-EXL…) en filas y horas (8–20) en columnas.

## Goals / Non-Goals

**Goals:**
- Una identidad visual propia, moderna y específica de aviación, aplicada a todas las plantillas.
- Que la tabla de vuelos, la pantalla más usada, sea lo más memorable y legible.
- CSS sin dependencias externas, mantenible con variables.

**Non-Goals:**
- Tema oscuro (el usuario eligió solo claro).
- Cambiar rutas, formularios, JS de comportamiento, modelos o scraping.
- Reescribir los HTML ya guardados en `static/html/`.
- Rediseñar el PDF (`export_to_pdf` mantiene su `<style>` en línea). La impresión desde el navegador de la página de la tabla sí entra (D9).
- Imprimir en horizontal o en color: se imprime en A4 vertical y en blanco y negro (decidido con el usuario).
- Resaltar la hora actual en la tabla (requeriría JS y conocer si el fichero es de hoy).

## Plan de diseño

**Supuesto de dirección:** aviación / torre de control, tema claro. El usuario pidió "bonito, moderno" y no eligió entre las direcciones propuestas; se tomó la recomendada porque nace del contenido real (horarios de aeronaves) y no de una plantilla.

**Color** (todos con contraste ≥ 4,5:1 sobre su fondo cuando llevan texto):

| Nombre | Hex | Uso |
|---|---|---|
| Carta | `#EEF3F7` | fondo de página (gris azulado frío, como una carta aeronáutica) |
| Papel | `#FFFFFF` | superficies: formularios, tabla |
| Tinta | `#0F1F2D` | texto principal y cabecera |
| Pizarra | `#4A5B6B` | texto secundario, etiquetas |
| Señal | `#1B5FAA` | acción principal y enlaces |
| Balizamiento | `#F5B800` | único acento cálido: marca de la cabecera y foco/hover de celdas con vuelo |
| Alerta | `#B3261E` | errores |
| Línea | `#C8D4DF` | bordes y separadores, y líneas verticales de la tabla |
| Línea fuerte | `#7B8C9B` | líneas horizontales entre filas de la tabla (3,46:1 sobre papel) |

**Tipografía:** una sola familia, **B612** (sans) y **B612 Mono**, diseñada por Airbus y ENAC para pantallas de cabina: legible a distancia y con formas inequívocas. Sans para interfaz y títulos (pesos 400/700); Mono solo para matrículas y horas, que son datos reales de la tabla. Escala modular 1.25 sobre 16 px; interlineado 1,5 en cuerpo; líneas de texto de menos de 70 caracteres. Se sirve desde `statics/fonts/` (OFL) en `woff2`, con pila de respaldo `system-ui, sans-serif`.

**Layout:** contenido alineado a la izquierda en una columna de hasta 64 rem, cabecera fija en el borde superior con la marca a la izquierda y "Cerrar sesión" a la derecha. Login, registro y agradecimiento usan un panel estrecho (24 rem) centrado verticalmente.

```
Vuelos                         Tabla
┌───────────────────────────┐  ┌────────────────────────────────────────┐
│ ▮ Planes         Salir    │  │ ▮ Planes                       Salir   │
├───────────────────────────┤  ├────────────────────────────────────────┤
│ Vuelos del 2026-10-12     │  │ vuelos-2026-10-12                      │
│ [Excel] [Tabla]           │  │ ┌──────────┬────┬─────┬─────┬─────┐   │
│ ¿Generar de nuevo?        │  │ │ Matrícula│  8 │  9  │ 10  │ …   │   │
│ [Día ▾]  [Generar]        │  │ ├──────────┼────┼─────┼─────┼─────┤   │
└───────────────────────────┘  │ │ EC-ERV   │    │09:00│     │11:10│   │
                               │ └──────────┴────┴─────┴─────┴─────┘   │
                               └────────────────────────────────────────┘
```

**Principios:**
1. Una sola cosa memorable: la tabla de vuelos. Es un panel de horarios, con una cabecera de horas estable, matrículas en mono y cada vuelo en una celda con su hora. Todo lo demás es sobrio.
2. El balizamiento amarillo aparece solo como marca de la cabecera y como realce al pasar por una celda con vuelo; no se usa para botones.
3. Sin gradientes decorativos, sin tarjetas idénticas ni sombras repetidas: las superficies se separan por borde de 1 px y por el fondo de la carta.
4. Movimiento solo donde responde a una acción: el indicador de carga. Nada de animaciones de entrada.

### Revisión del plan frente a los estilos genéricos

- Fondo crema + serif + terracota: descartado; el fondo es azul gris frío y la tipografía es sans de cabina.
- Oscuro con acento ácido: no aplica, el tema es claro.
- Tarjetas redondeadas idénticas con sombra suave: sustituidas por superficies planas con borde y un único radio (4 px) en controles; la tabla no es una tarjeta.
- Etiquetas pequeñas en mayúsculas, puntos medios y flechas "→": no se usan. Los títulos y etiquetas van en sentence case y los botones llevan un verbo ("Generar vuelos").
- Mono para etiquetas pequeñas: cambiado; el mono solo se aplica a datos (matrículas y horas), no a texto de interfaz.

Decisión de la revisión: el amarillo se reserva para la marca y el realce de celda; la acción principal va en azul Señal para que el amarillo conserve su valor de señal.

## Decisions

**D1. CSS propio con variables, sin Tailwind.**
Un único `styles.css` con `:root` de tokens (color, espacio, tipografía), seguido de capas por orden: base, componentes (`.btn`, `.field`, `.panel`, `.alert`, `.topbar`), páginas (`.auth`, `.flights`) y la tabla. Selectores de una clase (especificidad 0,1,0) para que el orden de la hoja decida y los componentes no se pisen entre sí.
*Alternativas:* mantener Tailwind y añadir CSS propio (sigue la dependencia del CDN y mezcla dos sistemas); migrar a Tailwind 3/4 (exige paso de compilación o CDN de desarrollo, no encaja con el despliegue Docker/Raspberry Pi actual sin build de front). Decisión tomada con el usuario.

**D2. Plantilla base única y `base_clean` como variante.**
`base.html` define cabecera (marca + acciones), `<main>` y los bloques `title`, `head`, `content`, `scripts`. `base_clean.html` pasa a extender `base.html` y solo cambia el contenedor a ancho completo y el bloque `scripts`. `page_500.html` e `index.html` extienden `base.html`. Esto elimina las tres cabeceras `<head>` duplicadas.
*Riesgo:* `page_500.html` se muestra cuando algo falla; debe seguir pintando aunque no haya sesión ni contexto. La cabecera no puede depender de `current_user` sin proteger; se resuelve mostrando "Cerrar sesión" solo si el contexto trae `current_user.is_authenticated` (Flask-Login lo inyecta, y `is_authenticated` existe también para anónimos).

**D3. La tabla se estiliza sobre `.dataframe`, no sobre una clase nueva.**
Los HTML guardados solo tienen `class="dataframe"`; estilizar esa clase cubre ficheros antiguos y nuevos sin reescribirlos. Una regla `.dataframe` (0,1,0) gana a los selectores de elemento del `<style>` en línea antiguo (0,0,1), así que no hace falta tocar esos ficheros. `generate_html_table` deja de añadir su `<style>` y el `<br/>`, y llama a `df.to_html(border=0)`; el título (`<h3>`) pasa a `<h1 class="table-title">`.
*Alternativa:* regenerar los ficheros antiguos (es destructivo y se descartó con el usuario).

**D4. Tabla en un contenedor desplazable con cabecera y primera columna fijas.**
`base_clean.html` envuelve el contenido en `.table-scroll` (`overflow-x: auto`). La fila de horas y la columna de matrículas usan `position: sticky`. `table.js` inserta una celda de controles como primera columna de cada fila, así que la columna de matrículas pasa a ser la segunda: la columna de controles se hace estrecha (ancho fijo de 2.75 rem, botones de icono con `aria-label`) y la columna de matrículas se fija con `left` igual a ese ancho.
*Alternativa:* convertir la tabla en tarjetas apiladas en móvil; pierde la visión de conjunto del día, que es el valor de la tabla.
El contenedor desplazable, los anchos mínimos y el `sticky` son solo de pantalla; al imprimir se anulan (D9).

**D5. Celdas con vuelo como "chips" de hora; vacías, vacías.**
Cada `td` con texto lleva B612 Mono, `font-variant-numeric: tabular-nums`, fondo azul muy claro y borde; la celda vacía no lleva borde ni fondo, así que la tabla se ve ligera y los vuelos destacan. Se hace solo con `:not(:empty)` sobre `td`, sin cambiar el HTML. Las celdas editables vuelven a `:empty`, de modo que añadir una fila no rompe la regla.
*Riesgo:* pandas escribe `<td></td>` para NaN, no `<td>NaN</td>`; verificado en `static/html/vuelos-2026-10-12.html`.

**D6. Indicador de carga con `role="status"`.**
El bloque `#loading` conserva su id y su clase `hidden`, pero incluye un anillo giratorio (CSS) y el texto "Extrayendo los datos. Puede tardar unos segundos." `role="status"` y `aria-live="polite"` lo anuncian al aparecer. La animación se desactiva con `@media (prefers-reduced-motion: reduce)`. `vuelos.js` no cambia.

**D7. Tipografía autoalojada.**
Los `.woff2` de B612 y B612 Mono (OFL, de Google Fonts) se guardan en `statics/fonts/` con `font-display: swap`. Sin CDN, funciona sin conexión y en la imagen Docker.
*Alternativa:* pila del sistema (más ligera pero pierde la identidad); Google Fonts por CDN (llamada externa).

**D8. Textos de interfaz revisados.**
Se mantienen los textos funcionales pero se unifican: botón "Generar vuelos" (hoy "Regenerar Vuelos" aunque aún no existan datos), "Cerrar sesión", "Iniciar sesión", "Descargar Excel", "Abrir tabla". Los errores dicen qué corregir: "Introduce un email válido", "La contraseña no es correcta". Se corrige "Username" por "Email" en el login, porque el campo es de tipo email.

**D9. Impresión: A4 vertical, la tabla se ajusta al ancho de la hoja.**
Causa del recorte actual: `.table-scroll` tiene `overflow: auto` y `max-height`, y cada columna tiene un ancho mínimo; en A4 vertical (≈190 mm útiles con 10 mm de margen) las 14 columnas no caben y el contenedor corta las últimas horas. Solución: un bloque `@media print` al final de `styles.css` con `@page { size: A4 portrait; margin: 10mm }`. Al imprimir: se ocultan `.topbar`, `.control-buttons`, `.table-toolbar` y los enlaces dentro de `.table-scroll` (el `home` suelto de los HTML antiguos); `.table-scroll` pasa a `overflow: visible; max-height: none`; la tabla usa `width: max-content` (con `max-width: 100%`), de modo que ocupa lo que pide su contenido y no toda la hoja: columnas de horas de 9 mm como mínimo y la de matrículas lo más estrecha posible, con el nombre largo ("Private booking") en dos líneas; se anula `sticky`; la letra baja a 7 pt con `white-space: nowrap` en las horas; `thead` con `display: table-header-group` y `tr` con `break-inside: avoid`.
*Alternativas:* escalar con `zoom` o `transform: scale` (resultado distinto entre navegadores y la impresión sigue recortada si no se calcula el factor); forzar A4 horizontal (el usuario imprime en vertical).

**D10. Cuadrícula más marcada, sin depender del color.**
En pantalla, el borde inferior de cada fila sube de `--linea` a `--linea-fuerte` (3,46:1 sobre papel, con 1 px) y las verticales se quedan en `--linea`, de modo que la horizontal domina. En impresión, las filas llevan `1px solid` en tinta oscura y las verticales un gris medio. Las celdas con vuelo pierden el fondo azul (los navegadores no imprimen fondos salvo con `print-color-adjust: exact`) y se distinguen por `border-left: 2px solid` en tinta y negrita. No se usa `print-color-adjust: exact`: gasta tóner y varía entre navegadores.
*Alternativa:* rayado cebra por fondo (no se imprime por defecto).

## Risks / Trade-offs

- [El navegador imprime con márgenes propios o escala distinta y la tabla sigue sin caber] → `width: max-content` con letra de 7 pt (el usuario encontró demasiado grande la versión de 8,5 pt a ancho completo); verificar con Chrome (vista previa o "Guardar como PDF") al 100 % y con "Ajustar a página".
- [Algún navegador ignora `@page { size }`] → No depender de él: la tabla se ajusta al ancho de la hoja que haya.
- [Se añaden columnas con la edición de `table.js` y la letra se vuelve ilegible] → Aceptado: el diseño cubre las 13 horas actuales; con muchas más columnas habría que imprimir en horizontal.
- [El `<style>` en línea de los HTML antiguos define `border` y `padding` de `th, td` también al imprimir] → Las reglas de impresión usan clase (0,1,x) y vencen a esos selectores de elemento; comprobarlo con los tres ficheros de `static/html/`.

- [El `<style>` en línea de los HTML antiguos pisa propiedades que mi CSS no defina] → Definir explícitamente `border`, `border-collapse`, `padding` y `text-align` en `.dataframe`, `.dataframe th` y `.dataframe td`, y comprobar visualmente los tres ficheros de `static/html/`.
- [La columna de controles de `table.js` rompe el `sticky` de matrículas] → Ancho fijo de la columna de controles y offset en una variable CSS; verificar con el navegador.
- [Las cifras de B612 Mono no se alinean como se espera] → Probar con horas reales; si no, usar `tabular-nums` sobre B612 sans.
- [Cambiar los textos de botones o etiquetas rompe a quien dependa de ellos (p. ej. Playwright de pruebas o scripts)] → Buscar referencias a esos textos en `test/` antes de cambiarlos.
- [Quitar Tailwind deja clases sin definir en alguna plantilla] → Quitar todas las clases de Tailwind de las plantillas y comprobar que no queda ninguna con `grep` de patrones típicos (`bg-`, `text-`, `px-`, `mb-`, `flex`).
- [Sin suite de tests, la regresión visual no se detecta sola] → Revisión manual con capturas a 360 px y 1280 px de cada página, y comprobación del flujo de punta a punta.

## Migration Plan

1. Implementar y comprobar en local con `flask run --debug`.
2. Desplegar con el flujo habitual (`docker compose up --build`). No hay migraciones de base de datos ni cambios de configuración.
3. Rollback: revertir el commit; los HTML de `static/html/` no se modifican, así que no hay datos que restaurar.

## Open Questions

- Si, tras ver las capturas, se prefiere otra dirección estética (editorial, cristal, oscuro), los tokens de color y tipografía están centralizados en `:root` y cambian sin tocar las plantillas.
