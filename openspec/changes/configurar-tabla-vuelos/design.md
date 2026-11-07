# Design

## Context

Estado actual (observado en el código):

- `clas_to_series()` (`src/app/utils/utils.py`) construye un `DataFrame` con una columna por hora. `replace_salidas()` genera 24 posiciones y `delete_0_salidas()` las recorta con `START_DEL=8` / `END_DEL=3` (`src/core/settings.py`), es decir, horas 8 a 20. Ese recorte llega al HTML (`generate_html_table` → `df.to_html`) y al Excel, que salen del mismo `DataFrame`.
- La tabla se sirve en `/table/<fichero>` (`page_html_table`, `src/auth/routes.py`): lee `static/html/vuelos-<fecha>.html` y lo inyecta en `base_clean.html`. La ruta **no** exige sesión. Los HTML ya guardados contienen solo las horas 8–20.
- `src/auth/statics/js/table.js` trabaja sobre `.dataframe`, añade los controles de fila y **añade una fila al final del `tbody`** con el botón de edición (`addToggleEditButton`).
- Las celdas con vuelo contienen la hora completa (`"09:30"`); las vacías, `CARACTER_NOT_FLIGHT`. La cabecera es una fila de `<th>` con el número de hora y la primera celda de cada fila es un `<th>` con la matrícula.
- SQLAlchemy + Flask-Migrate; modelos en `src/auth/models/`. No hay tabla de aviones: las matrículas solo existen dentro del HTML de cada día.
- Spec existente `web-interface` exige que la tabla se imprima completa (A4 vertical) en tablas nuevas y antiguas.

## Goals / Non-Goals

**Goals:**
- Configuración por usuario (rango de horas y matrículas ocultas) persistida en PostgreSQL y aplicada a cualquier día.
- Funcionar igual con los HTML antiguos (8–20 h) y con los nuevos (24 h).
- Sin parpadeo: la tabla llega ya filtrada al navegador.

**Non-Goals:**
- No se regeneran ni se reescriben los HTML antiguos.
- No se crea un catálogo de aviones en la base de datos ni se sustituye la lista `No_Plane` (exclusión global del scraper).
- No se cambia el rango del Excel ni de la descarga.
- No hay preferencias por día ni administración de preferencias de otros usuarios.
- No se añade ningún framework de frontend.

## Decisions

### 1. Filtrar en el navegador, con el HTML completo como fuente
El HTML guardado sigue siendo la única fuente de datos; las columnas y filas se ocultan en cliente con `table.js` (y una clase `is-hidden` / atributo `hidden`), no se vuelven a generar.
- **Por qué**: las matrículas existen solo en el HTML de cada día; cambiar la configuración no debe re-ejecutar ni depender del scraper, y funciona igual con tablas antiguas. Los avisos de "hay vuelos previos/posteriores" salen de las propias celdas.
- **Alternativa descartada**: filtrar en servidor reescribiendo el HTML en `page_html_table`. Obliga a parsear HTML con BeautifulSoup en cada petición y duplica la lógica de aviso; solo gana evitar el parpadeo, que se resuelve con la decisión 3.

### 2. Las columnas de hora se identifican por la cabecera, no por posición
`table.js` lee el texto de cada `<th>` de la fila de cabecera como número de hora y mapea índice de columna → hora. La matrícula es el `<th>` de cada fila de `tbody`. Así vale para HTML antiguos y nuevos, y no depende de `START_DEL`.
- **Alternativa descartada**: añadir `data-hour` al generar. Solo serviría para tablas nuevas; habría que mantener dos caminos.
- El script no debe confundirse con las columnas de controles que inserta `addRowControls` (se excluyen por la clase `control-buttons`) ni con celdas añadidas en edición.

### 3. Preferencias inyectadas en la página, API JSON para guardarlas
`page_html_table` consulta las preferencias del `current_user` y las pasa a la plantilla como JSON en un `<script type="application/json">`; `table.js` las aplica antes del primer pintado (el contenedor de la tabla se oculta por CSS hasta que `table.js` marca la tabla como lista, y un `<noscript>` la muestra completa). Guardar:
- `GET /table/preferences` → `{hour_start, hour_end, hidden_planes}` (valores por defecto si no hay fila).
- `PUT /table/preferences` con ese mismo JSON → valida y hace upsert. 401 sin sesión, 400 con rango inválido.
Ambos en `auth_bp`, con `@login_required`. `page_html_table` no pasa a exigir login (se respeta el comportamiento actual; la spec pide verla sin controles); sin sesión recibe los valores por defecto.
- **Por qué PUT del objeto completo**: es idempotente y evita carreras entre campos; la configuración es pequeña.
- La ruta literal `/table/preferences` debe registrarse de modo que no choque con `/table/<string:file_name>` (Flask prioriza la regla estática; se verifica en la tarea correspondiente).

### 4. Modelo: una fila por usuario
Tabla `table_preferences`: `id`, `user_id` (FK `users.id`, único, `ON DELETE CASCADE`), `hour_start` smallint (default 8), `hour_end` smallint (default 20), `hidden_planes` JSONB (default `[]`), `updated_at`. `CHECK (hour_start BETWEEN 0 AND 23 AND hour_end BETWEEN 0 AND 23 AND hour_start <= hour_end)`.
- Se guarda la lista de **ocultas**, no la de visibles, para que una avioneta nueva se muestre por defecto (spec: "Matrícula nueva").
- **Alternativa descartada**: columnas `JSON` genéricas de "settings" o fila por matrícula. Más flexible pero sobredimensionado; no hay otro ajuste previsto.
- Los valores por defecto 8 y 20 se derivan de `settings.START_DEL` y `24 - 1 - settings.END_DEL` en una sola función, para no duplicar números.
- Validación en el servidor (enteros 0–23, inicial ≤ final, `hidden_planes` lista de cadenas de longitud acotada); el `CHECK` es el último cinturón.

### 5. Las tablas nuevas se generan con 24 horas; el Excel no cambia
En `clas_to_series()` el `DataFrame` se construye con las 24 horas para el HTML. El Excel se escribe con el recorte `[START_DEL : 24-END_DEL]` actual, para no alterar lo que descargan los usuarios. `delete_0_salidas` se conserva solo para el Excel o se sustituye por un slice de columnas del `DataFrame`.
- **Por qué**: sin horas fuera de 8–20 en el HTML, "ampliar el rango" sería imposible en tablas nuevas.
- **Efecto**: las columnas de 0–7 y 21–23 existen en el DOM pero se ocultan por defecto (rango 8–20), de modo que la vista por defecto es idéntica a la actual.
- Las tablas antiguas limitan los selectores de hora a las horas presentes (spec: "Tabla guardada antes del cambio").

### 6. Confirmaciones con `<dialog>` nativo, no `alert/confirm`
El diálogo de matrículas y el aviso de vuelos fuera de rango usan el elemento `<dialog>` (`showModal()`): da foco atrapado, Escape y backdrop sin librerías, y se estila con los tokens existentes de `styles.css`. `window.confirm` se descarta porque no admite el texto detallado, no se puede estilar y rompe pruebas de navegador automatizadas.
- El aviso decide con las celdas: un vuelo existe en la hora *h* si alguna celda de esa columna no está vacía y no es `CARACTER_NOT_FLIGHT` (se compara con el contenido recortado). Solo cuentan los vuelos de **matrículas visibles**; los de matrículas ocultas no generan aviso.

### 7. Barra de herramientas fuera de la tabla
`table.js` crea un `<div class="table-toolbar" role="toolbar">` antes de `.table-scroll` y se elimina `addToggleEditButton` del final del `tbody`. `toggleEditMode` pasa a leer su botón por id sin depender de su posición. La barra se oculta en `@media print`.
- **Por qué fuera**: dentro de `<table>` queda dentro del scroll y se desplaza con la tabla; fuera, permanece visible. El CSS actual `.dataframe .table-toolbar` (celda) se reutiliza solo en nombre; se reescribe como bloque independiente.
- Los controles de Horas y Avionetas solo se renderizan si `current_user.is_authenticated` (dato en el JSON de la decisión 3).

### 8. Impresión
Las columnas/filas ocultas usan `display: none` también en `@media print`. La impresión actual usa `table-layout: auto` y `width: max-content`, por lo que el ancho se recalcula solo con las columnas visibles; no hay que tocar la regla de escala, solo comprobarlo en la vista previa.

## Risks / Trade-offs

- **Hay un Flask accesible en `0.0.0.0:5000` apuntando a la base de producción** (según el estado de la sesión) → la migración debe probarse primero en la base local (`docker-compose.db.yml`, `DATABASE_HOST=localhost`) y aplicarse en producción solo con confirmación explícita. Mientras se desarrolla, conviene apagar esa instancia o usar la base local.
- **Tablas viejas sin horas fuera de 8–20** → el usuario con rango 6–22 verá una tabla "más corta" que lo configurado. Mitigado: los selectores se limitan a las horas presentes y se explica en la interfaz.
- **Conflicto de rutas `/table/preferences` y `/table/<file_name>`** → se usa otro prefijo (`/preferences/table`) si Flask resuelve mal. Se decide en implementación con una prueba manual; no cambia la spec.
- **Parpadeo / tabla sin JS** → contenedor oculto hasta aplicar preferencias, con `<noscript>` de respaldo.
- **Impresión con pocas columnas** → se verifica en la vista previa con un rango reducido y matrículas ocultas.
- **La migración se aplica sola en producción** (`entrypoint.sh`) → un fallo de la migración impide arrancar el contenedor; por eso se prueba upgrade/downgrade en local antes.
- **Matrículas con espacios o tabuladores** (algunas entradas de `No_Plane` los traen) → las matrículas se normalizan con `strip()` al leerlas del DOM y al guardarlas.
- **Sin suite de tests** (el proyecto no tiene) → la verificación es manual; las funciones puras (validar y normalizar preferencias) se aíslan para poder probarlas con un script suelto.

## Migration Plan

1. Crear el modelo `TablePreferences` y generar la migración con `flask db migrate`; revisar el SQL a mano (FK, `CHECK`, defaults).
2. Aplicar en local: `docker compose -f docker-compose.db.yml up -d` + `flask db upgrade`; probar upgrade y downgrade.
3. Desplegar el código. `entrypoint.sh` ejecuta `flask db upgrade` en cada arranque del contenedor, así que la migración se aplica sola al desplegar: debe estar probada en local (upgrade y downgrade) antes de fusionar.
4. **Rollback**: `flask db downgrade` elimina `table_preferences`; el código anterior ignora la tabla. Los HTML ya generados no se tocan, así que no hay nada que restaurar.
5. Los HTML con 24 horas solo aparecen al regenerar un día; los anteriores siguen válidos.
