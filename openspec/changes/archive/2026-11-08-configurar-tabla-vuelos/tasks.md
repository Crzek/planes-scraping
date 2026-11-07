# Tasks

## 1. Modelo y migración

- [x] 1.1 Crear el modelo `TablePreferences` en `src/auth/models/table_preferences.py` (`user_id` único con FK a `users` y `ON DELETE CASCADE`, `hour_start`, `hour_end`, `hidden_planes` JSONB, `updated_at`, `CHECK` de rango) e importarlo en `create_app()` junto a `User`; verificar que `python -c "from src.auth.models.table_preferences import TablePreferences"` importa sin error
- [x] 1.2 Generar la migración con `flask db migrate -m "table preferences"` contra la base **local** (`DATABASE_HOST=localhost`), revisar a mano el SQL (FK, `CHECK`, defaults) y verificar que `flask db upgrade` y `flask db downgrade` funcionan y dejan la tabla creada/eliminada (`\d table_preferences` en `psql` dentro de `planes-db-local`)

## 2. Lógica y API de preferencias

- [x] 2.1 Añadir en `src/auth/` funciones puras para valores por defecto (derivados de `settings.START_DEL`/`END_DEL`), validar y normalizar un payload (enteros 0–23, inicial ≤ final, `hidden_planes` lista de cadenas con `strip()` y longitud acotada); verificar con un script suelto que acepta 8/20, rechaza 10/8 y 24, y normaliza `"EC-IXA\t"`
- [x] 2.2 Implementar `GET` y `PUT /table/preferences` en `src/auth/routes.py` con `@login_required`, upsert por `current_user.id`, 400 con mensaje por campo y 401 sin sesión, y registro de logs con `logger`; verificar con `curl` autenticado (GET devuelve defaults, PUT persiste, PUT inválido devuelve 400, sin cookie devuelve 401) y que `/table/vuelos-<fecha>.html` sigue resolviendo a `page_html_table`
- [x] 2.3 Hacer que `page_html_table` cargue las preferencias de `current_user` (o los defaults sin sesión) y las pase a `base_clean.html` como JSON junto con `authenticated`; verificar con la vista fuente de la página que el JSON aparece y que sin sesión llega `authenticated: false`

## 3. Generación de la tabla con 24 horas

- [x] 3.1 En `clas_to_series()` construir el `DataFrame` con las 24 horas para el HTML y escribir el Excel con el recorte `START_DEL`/`END_DEL` actual (ajustar `replace_salidas`/`delete_0_salidas` y el `index=range(...)`); verificar regenerando un día que el HTML tiene `<th>` de 0 a 23 y que el Excel descargado conserva las columnas 8 a 20 sin cambios

## 4. Barra de herramientas y filtrado en la tabla

- [x] 4.1 En `src/auth/statics/js/table.js` crear la barra de herramientas antes de `.table-scroll`, mover a ella el botón de edición y eliminar `addToggleEditButton` del final del `tbody`; verificar en el navegador que el botón está encima de la tabla, que no queda ninguno al final y que habilitar/deshabilitar edición sigue mostrando y ocultando los controles de fila
- [x] 4.2 Mapear columnas de hora por el texto de la cabecera y matrículas por el `<th>` de cada fila (excluyendo `control-buttons`), y aplicar las preferencias iniciales ocultando columnas/filas fuera de ellas antes del primer pintado (contenedor oculto hasta estar listo, `<noscript>` de respaldo); verificar con una tabla nueva y una guardada (8–20) que el rango por defecto se ve igual que antes
- [x] 4.3 Añadir el control **Horas** (selectores de inicio y fin limitados a las horas presentes), la validación de inicio ≤ fin y el aviso con `<dialog>` cuando se ocultan horas con vuelos de matrículas visibles (Aceptar guarda con `PUT`, Cancelar restaura selectores y tabla); verificar los cuatro escenarios de la spec (previos, posteriores, sin vuelos fuera, cancelar) en el navegador
- [x] 4.4 Añadir el control **Avionetas**: `<dialog>` con una casilla etiquetada por matrícula (incluye las ocultas), bloqueo de confirmar sin ninguna marcada, Cancelar/Escape sin cambios y guardado con `PUT`; verificar que ocultar una matrícula quita su fila, que se conserva al abrir otro día y que una matrícula nueva aparece visible
- [x] 4.5 Manejar errores de guardado (respuesta no OK o fallo de red): mostrar un mensaje visible, no aplicar el cambio y mantener la configuración anterior; verificar parando la base local o simulando un 500 y comprobando que la tabla no cambia
- [x] 4.6 Mostrar los controles Horas y Avionetas solo si `authenticated`; verificar en una ventana sin sesión que solo aparece el botón de edición y que un `PUT` sin cookie devuelve 401

## 5. Estilos e impresión

- [x] 5.1 En `src/auth/statics/styles/styles.css` estilar la barra de herramientas (con tokens existentes, áreas táctiles de 44 px, varias líneas en 360 px), los `<dialog>` (título, foco visible, backdrop) y las clases de ocultación; reescribir `.dataframe .table-toolbar` y quitarlo de las reglas de impresión que ya no aplican; verificar a 360 px sin desplazamiento horizontal y con navegación solo por teclado (foco visible, Escape devuelve el foco al botón)
- [x] 5.2 Asegurar que en `@media print` se oculta la barra de herramientas y los diálogos y que las columnas/filas ocultas no se imprimen; verificar en la vista previa de impresión (A4 vertical) con el rango por defecto (13 columnas de hora) y con rango 10–16 y una matrícula oculta

## 6. Documentación y verificación final

- [x] 6.1 Documentar en `CLAUDE.md` (sección de arquitectura) el modelo `TablePreferences`, los endpoints y que `START_DEL`/`END_DEL` son ahora los valores por defecto; verificar que el texto coincide con el código
- [x] 6.2 Recorrido de integración con la base local: dos usuarios con rangos distintos, persistencia tras cerrar sesión y entrar desde otro navegador, tabla antigua y tabla nueva, descarga del Excel intacta; verificar cada escenario de `specs/flight-table-preferences/spec.md` y `specs/web-interface/spec.md`
- [x] 6.3 Ejecutar `openspec validate configurar-tabla-vuelos --strict` y verificar que no da errores

## Workflow follow-up

- Aplicar la migración en producción solo tras confirmarlo con la persona responsable; `entrypoint.sh` la ejecuta al arrancar el contenedor.
- Archivar el cambio cuando se haya revisado y verificado.
