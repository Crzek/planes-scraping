# Tasks

## 1. Base visual: tokens, tipografía y componentes

- [x] 1.1 Descargar B612 y B612 Mono (OFL) en `woff2` a `src/auth/statics/fonts/` y declarar los `@font-face` con `font-display: swap`; verificar que el navegador las carga (pestaña Red, sin peticiones externas)
- [x] 1.2 Escribir en `src/auth/statics/styles/styles.css` el bloque `:root` con los tokens de color, tipografía (escala 1.25), espaciado y radio de design.md, más el reset y los estilos base de `body`, enlaces y títulos; verificar que el contraste de texto y enlaces es ≥ 4,5:1 con una herramienta de contraste
- [x] 1.3 Añadir los componentes `.topbar`, `.btn`, `.field`, `.panel`, `.alert` y el foco visible, con selectores de una clase; verificar en un HTML de prueba que cada componente se ve bien y que Tab muestra el foco
- [x] 1.4 Añadir `prefers-reduced-motion` y las reglas responsive base (360 px sin desplazamiento horizontal); verificar con el navegador a 360 px y con la preferencia activada

## 2. Plantillas base y páginas de acceso

- [x] 2.1 Reescribir `src/auth/templates/base.html` (`lang="es"`, enlace a `styles.css` con `url_for('authBP.static', ...)`, cabecera con marca y "Cerrar sesión" solo si hay sesión, `<main>`, sin Tailwind) y verificar que `/login` carga sin errores en la consola
- [x] 2.2 Convertir `base_clean.html` en extensión de `base.html` con contenedor `.table-scroll` y el bloque `scripts` de `table.js`; verificar que `/table/<fichero>` carga la tabla y `table.js` sigue añadiendo los controles
- [x] 2.3 Rediseñar `login.html` y `register.html` (panel estrecho, etiquetas asociadas, errores junto al campo con texto que dice qué corregir, "Email" en lugar de "Username"); verificar login con datos erróneos y un registro de prueba
- [x] 2.4 Rediseñar `thanks.html`, `generic_content.html` y `page_404.html` con la base común; verificar abriendo `/hora` (o la ruta de contenido genérico), una URL inexistente y la página de gracias tras registrarse
- [x] 2.5 Hacer que `page_500.html` y `src/app/templates/index.html` extiendan `base.html`; verificar `/scrapy` y forzando un error 500 en local que se ven con estilo y sin fallar

## 3. Página de vuelos y estado de carga

- [x] 3.1 Rediseñar `vuelos.html` y `form_vuelos.html` (título, enlaces "Descargar Excel" y "Abrir tabla", mensaje de datos ya existentes, botón "Generar vuelos", `select` y casilla con etiquetas visibles), conservando los ids y nombres de campo; verificar que el POST sigue enviando `day` y `select_all`
- [x] 3.2 Añadir el indicador de carga en `#loading` (anillo CSS, texto "Extrayendo los datos. Puede tardar unos segundos.", `role="status"`) sin tocar `vuelos.js`; verificar que al enviar el formulario se oculta el formulario y aparece el indicador, y que con movimiento reducido no gira
- [x] 3.3 Probar el flujo completo en local (login → generar vuelos de hoy → descargar Excel → abrir tabla) y confirmar que cada paso funciona como antes

## 4. Tabla de vuelos

- [x] 4.1 Estilizar `.dataframe` (bordes, cabecera de horas fija, columna de matrículas fija con offset por la columna de controles, celdas con vuelo como chips en B612 Mono con `tabular-nums`, celdas vacías sin borde ni fondo, realce amarillo al pasar); verificar visualmente con los tres ficheros de `static/html/`, que el `<style>` en línea antiguo no pisa el resultado
- [x] 4.2 Estilizar los controles de `table.js` (`.control-buttons`, botones de icono con `aria-label`) y ajustar `table.js` solo si hace falta para añadir esas clases y etiquetas; verificar que añadir y eliminar fila siguen funcionando y que la nueva fila usa el mismo estilo
- [x] 4.3 Actualizar `generate_html_table` en `src/app/utils/export.py` para quitar el `<style>`, el `<br/>` y el `border="1"` (`df.to_html(border=0)`), con el título como `<h1 class="table-title">`; dejar `export_to_pdf` igual; verificar generando un día nuevo y abriendo su tabla
- [x] 4.4 Marcar la cuadrícula (D10): añadir el token `--linea-fuerte` en `styles.css`, usarlo en el borde inferior de las filas de `.dataframe` y dejar las verticales en `--linea`; verificar en el navegador con los tres ficheros de `static/html/` que cada fila se separa con claridad y que la línea contrasta ≥ 3:1 con el papel
- [x] 4.5 Añadir el bloque `@media print` (D9 y D10) al final de `styles.css`: A4 vertical, ocultar cabecera, enlace `home`, controles y toolbar, tabla compacta al ancho de su contenido con letra de 7 pt y primera columna estrecha, fila de horas repetida y filas sin partir, líneas oscuras, celdas con vuelo con borde izquierdo y negrita sin fondo; verificar con Chrome (vista previa o "Guardar como PDF") que `vuelos-2026-10-12.html` sale con la columna de matrículas y las 13 horas en una sola hoja A4 vertical
- [x] 4.6 Comprobar la impresión en blanco y negro (sin gráficos de fondo) con los otros dos HTML guardados y con una tabla con más filas que una hoja; verificar que la fila de horas se repite, ninguna fila se parte y las celdas con vuelo se distinguen de las vacías

## 5. Limpieza y comprobación final

- [x] 5.1 Buscar con `grep` clases de Tailwind restantes (`bg-`, `text-`, `px-`, `mb-`, `flex`, `shadow`) y la URL del CDN en `src/` y borrar las que queden; verificar que no hay coincidencias
- [x] 5.2 Buscar referencias a los textos de botones y etiquetas cambiados en `test/` y en scripts de automatización, y adaptarlas si existen; verificar con `grep` que no queda ninguna rota
- [x] 5.3 Revisar cada página a 360 px y a 1280 px con capturas (login, registro, gracias, vuelos vacío, vuelos con resultados, tabla, 404, 500, inicio) y comprobar navegación con teclado; verificar que ninguna se desplaza en horizontal salvo la tabla dentro de su contenedor
- [x] 5.4 Reconstruir la imagen con `docker compose up --build` y comprobar que las fuentes y la hoja de estilos se sirven correctamente; verificar que `docker logs` no muestra errores 404 de estáticos

## Workflow follow-up

- Archivar el cambio cuando se haya revisado en local y en el servidor.
