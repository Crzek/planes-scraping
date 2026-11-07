# Proposal

## Why

La tabla de vuelos (`/table/vuelos-<fecha>.html`) muestra siempre las mismas columnas de horas, las de `START_DEL=8` a `24-END_DEL=3` (de 8 a 20 h), fijadas en el código y horneadas en el HTML guardado, y todas las matrículas sin excepción. Quien la consulta o la imprime no puede quitar las horas ni las avionetas que no le interesan, y el botón de "Habilitar edición" está al final de la tabla, donde hay que desplazarse para encontrarlo. Hace falta que cada usuario decida qué ve y que su elección se recuerde.

## What Changes

- El botón de habilitar/deshabilitar edición pasa del final de la tabla a una barra de herramientas encima de ella, siempre visible.
- Nueva opción **Horas** en esa barra: el usuario elige la hora inicial y la hora final de las columnas que se muestran, en lugar del rango fijo de 8 a 20 h.
- Si el nuevo rango deja fuera horas que sí tienen vuelos (antes de la hora inicial o después de la final), la tabla pide confirmación con un aviso ("hay vuelos previos/posteriores, ¿seguro que no quieres verlos?") con **Aceptar** y **Cancelar**. Cancelar deja el rango como estaba.
- Nueva opción **Avionetas** en la barra: abre un diálogo con todas las matrículas de la tabla y una casilla por cada una. Las desmarcadas se ocultan de la tabla.
- La configuración (rango de horas y matrículas ocultas) se guarda en la base de datos por usuario y se aplica al abrir cualquier tabla, de cualquier día.
- Las tablas nuevas se generan con las 24 horas del día para que el rango pueda ampliarse más allá de 8–20 h; el Excel conserva su rango actual. Las tablas ya guardadas (solo 8–20 h) siguen funcionando, con el rango limitado a las horas que contienen.
- La impresión respeta la configuración: solo se imprimen las columnas y filas visibles.
- Nueva migración de Alembic con la tabla de preferencias.

## Capabilities

### New Capabilities
- `flight-table-preferences`: preferencias de visualización de la tabla de vuelos por usuario (rango de horas y matrículas visibles), su persistencia en la base de datos, su API y las confirmaciones al ocultar horas con vuelos.

### Modified Capabilities
- `web-interface`: la barra de herramientas de la tabla (botón de edición arriba, accesos a Horas y Avionetas, diálogo de matrículas) y la impresión, que pasa a imprimir solo lo visible (cambia el requisito "La tabla de vuelos se imprime completa").

## Impact

- **Código**: `src/auth/routes.py` (ruta `page_html_table` y nuevos endpoints de preferencias), nuevo modelo en `src/auth/models/` y migración en `migrations/versions/`, `src/app/utils/utils.py` y `src/app/utils/export.py` (generar 24 h en el HTML y mantener el Excel), `src/auth/statics/js/table.js`, `src/auth/statics/styles/styles.css`, `src/auth/templates/base_clean.html`.
- **Base de datos**: tabla nueva `table_preferences` (clave foránea a `users`). La migración debe aplicarse primero a la base local y solo después a producción: el `.env` actual apunta a producción.
- **API**: dos endpoints JSON nuevos (leer y guardar preferencias), protegidos por sesión.
- **Compatibilidad**: los HTML de `static/html/` existentes siguen sirviéndose sin regenerarlos; `START_DEL` y `END_DEL` pasan a ser solo los valores por defecto.
- **Sin dependencias nuevas**.
