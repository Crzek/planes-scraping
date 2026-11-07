# Proposal

## Why

Todas las páginas de la web se ven con el aspecto por defecto de Tailwind 2.2.19 (fondo gris, botón azul, formulario blanco con sombra) y no tienen identidad visual. `styles.css` está vacío, `index.html` y `page_500.html` no tienen ningún estilo, y la tabla de vuelos, que es la pantalla más útil, es una tabla con bordes negros de 1 px. La herramienta la usa personal de operaciones del aeropuerto de Sabadell, y el aspecto debería ser a la vez moderno, agradable y fácil de leer de un vistazo.

## What Changes

- Sistema de diseño propio en `src/auth/statics/styles/styles.css`: variables CSS (color, tipografía, espaciado, radios), componentes (botón, campo de formulario, tarjeta, enlace, mensaje de error, tabla) y reglas responsive. Reemplaza a Tailwind.
- Dirección estética: aviación / torre de control, tema claro, con tipografía técnica para horas y matrículas. Es un supuesto, porque el usuario no eligió dirección entre las opciones propuestas; se puede cambiar antes de implementar.
- Rediseño de **todas** las plantillas Jinja: `base.html`, `base_clean.html`, `login.html`, `register.html`, `thanks.html`, `vuelos.html`, `form_vuelos.html`, `generic_content.html`, `page_404.html`, `page_500.html` y `src/app/templates/index.html`.
- Se elimina la dependencia de Tailwind por CDN: sin la hoja externa, la web funciona sin conexión y sin depender de una versión antigua.
- `page_500.html` e `index.html` pasan a heredar de la base común (hoy son HTML suelto sin estilos).
- La tabla de vuelos (`generate_html_table` en `src/app/utils/export.py`) deja de incrustar su `<style>` básico: pasa a usar el estilo de la hoja común. Los HTML ya guardados en `static/html/` no se reescriben; se muestran dentro de `base_clean.html` con el nuevo estilo. `export_to_pdf` no cambia: el PDF no carga la hoja de estilos del sitio y necesita su `<style>` en línea.
- La página de la tabla de vuelos se puede **imprimir completa** en una hoja A4 vertical (hoy el navegador la recorta y solo salen las primeras horas), sin la cabecera del sitio ni los controles de edición, y con las líneas de fila más marcadas para seguir cada matrícula hasta su hora. Pensado para imprimir en blanco y negro.
- Se conservan sin cambios de comportamiento: los nombres de campos y ids de formulario, `.dataframe` y los botones de edición de `table.js`, los ids que usa `vuelos.js` (`vuelosForm`, `remakeForm`, `loading`, `container-form`) y todas las rutas.
- Se corrige la accesibilidad de base: `lang="es"`, foco de teclado visible, contraste suficiente, `prefers-reduced-motion` respetado y diseño usable en móvil.

## Capabilities

### New Capabilities
- `web-interface`: apariencia y usabilidad de las páginas HTML que sirve la aplicación (identidad visual común, componentes, tabla de vuelos legible, estados de carga/error/vacío, accesibilidad y responsive).

### Modified Capabilities
<!-- Ninguna: los specs existentes (container-image, flight-data-acquisition, runtime-logging) no cambian. -->

## Impact

- Código afectado: `src/auth/templates/*.html`, `src/app/templates/index.html`, `src/auth/statics/styles/styles.css`, `src/auth/statics/js/table.js` y `vuelos.js` (solo ajustes menores de clases), `src/app/utils/export.py`.
- Sin cambios en rutas, modelos, base de datos ni scraping.
- Dependencias: se elimina el CDN de Tailwind. Si se usan fuentes web, se sirven desde `static` propio o con una pila de fuentes del sistema, para no añadir llamadas externas ni romper el despliegue en Docker/Raspberry Pi.
- Riesgo: los HTML antiguos de `static/html/` llevan su propio `<style>` en línea que puede pisar parte del nuevo estilo; el diseño debe convivir con ellos.
