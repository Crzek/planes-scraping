const table = document.querySelector(".dataframe");

// Función para agregar botones de control a cada fila
function addRowControls(row) {
    const controlCell = document.createElement("td");
    controlCell.classList.add("control-buttons", "no-edit"); // Clase para identificar la columna no editable
    controlCell.innerHTML = `
        <button type="button" class="row-btn" onclick="addRowBelow(this)" aria-label="Añadir fila debajo" title="Añadir fila debajo">+</button>
        <button type="button" class="row-btn row-btn--danger" onclick="deleteSpecificRow(this)" aria-label="Eliminar fila" title="Eliminar fila">&times;</button>
    `;
    row.insertBefore(controlCell, row.firstChild);
}

// Función para inicializar los controles en filas existentes
function initializeRowControls() {
    const rows = table.querySelectorAll("tbody tr, thead tr");
    rows.forEach((row) => {
        addRowControls(row); // Agregar controles a cada fila existente
    });
}

// Función para agregar una fila debajo de la fila actual
function addRowBelow(button) {
    const currentRow = button.closest("tr");
    const newRow = document.createElement("tr");

    // Agregar una celda de control a la nueva fila
    addRowControls(newRow);

    // Agregar celdas vacías para cada columna existente
    const columnCount = table.rows[0].cells.length - 1; // Excluir la columna de controles
    for (let i = 0; i < columnCount; i++) {
        const cell = document.createElement("td");
        cell.textContent = ""; // Celda vacía
        newRow.appendChild(cell);
    }

    currentRow.parentNode.insertBefore(newRow, currentRow.nextSibling);
    applyView();
}

// Función para eliminar una fila específica
function deleteSpecificRow(button) {
    const currentRow = button.closest("tr");
    currentRow.parentNode.removeChild(currentRow);
}

// Función para agregar una fila
function addRow() {
    const tbody = table.querySelector("tbody");
    const newRow = document.createElement("tr");

    // Agregar una celda de encabezado para la nueva fila
    const headerCell = document.createElement("th");
    headerCell.textContent = "Nuevo Avión";
    newRow.appendChild(headerCell);

    // Agregar celdas vacías para cada columna existente
    const columnCount = table.rows[0].cells.length - 1; // Excluir el encabezado vacío
    for (let i = 0; i < columnCount; i++) {
        const cell = document.createElement("td");
        cell.textContent = ""; // Celda vacía
        newRow.appendChild(cell);
    }

    // Agregar botones de control a la nueva fila
    addRowControls(newRow);

    tbody.appendChild(newRow);
    applyView();
}

// Función para agregar una columna
function addColumn() {
    // Agregar un encabezado para la nueva columna
    const headerRow = table.rows[0];
    const newHeader = document.createElement("th");
    newHeader.textContent = `Nueva Columna`;
    headerRow.appendChild(newHeader);

    // Agregar celdas vacías a cada fila del cuerpo
    for (let i = 1; i < table.rows.length; i++) {
        const cell = document.createElement("td");
        cell.textContent = ""; // Celda vacía
        table.rows[i].appendChild(cell);
    }
}

// Función para eliminar una fila
function deleteRow() {
    const tbody = table.querySelector("tbody");
    if (tbody.rows.length > 0) {
        tbody.deleteRow(-1); // Eliminar la última fila
    } else {
        alert("No hay más filas para eliminar.");
    }
}

// Función para eliminar una columna
function deleteColumn() {
    const columnCount = table.rows[0].cells.length;
    if (columnCount > 1) {
        // Eliminar la última columna de cada fila
        for (let i = 0; i < table.rows.length; i++) {
            table.rows[i].deleteCell(-1);
        }
    } else {
        alert("No hay más columnas para eliminar.");
    }
}

// Función para habilitar la edición de celdas al hacer clic
function enableCellEditing() {
    const cells = table.querySelectorAll("tbody td:not(.no-edit), tbody th"); // Excluir la columna de botones
    cells.forEach((cell) => {
        cell.addEventListener("click", () => {
            const currentValue = cell.textContent.trim(); // Guardar el valor actual
            const input = document.createElement("input");
            input.type = "text";
            input.value = currentValue; // Establecer el valor actual en el campo de entrada

            // Guardar el nuevo valor al perder el foco
            input.addEventListener("blur", () => {
                if (input.value.trim() === "") {
                    cell.textContent = currentValue; // Restaurar el valor original si está vacío
                } else {
                    cell.textContent = input.value; // Guardar el nuevo valor
                }
                cell.addEventListener("click", enableCellEditing); // Rehabilitar el evento
            });

            // Cancelar edición si se presiona Escape
            input.addEventListener("keydown", (event) => {
                if (event.key === "Escape") {
                    cell.textContent = currentValue; // Restaurar el valor original
                    cell.addEventListener("click", enableCellEditing); // Rehabilitar el evento
                }
            });

            // Reemplazar el contenido de la celda con el campo de entrada
            cell.textContent = ""; // Limpiar el contenido actual
            cell.appendChild(input);
            input.focus();
        });
    });
}

// Función para alternar (toggle) entre habilitar/deshabilitar edición
function toggleEditMode() {
    const controlButtons = table.querySelectorAll(".control-buttons");
    const cells = table.querySelectorAll("tbody td:not(.no-edit)"); // Excluir la columna de botones
    const editButton = document.getElementById("edit-btn");

    // Determinar si actualmente está habilitada la edición
    const isEditingEnabled = cells[0]?.isContentEditable;

    // Alternar visibilidad de los botones de control
    controlButtons.forEach((buttonCell) => {
        buttonCell.style.display = isEditingEnabled ? "" : "none";
    });
    // el CSS desplaza la columna fija de matrículas solo si los controles se ven
    table.classList.toggle("has-controls", Boolean(isEditingEnabled));

    // Alternar entre habilitar/deshabilitar edición
    cells.forEach((cell) => {
        if (cell.classList.contains("no-edit")) return; // No editar las celdas de control
        cell.contentEditable = !isEditingEnabled; // Alternar el estado de edición
    });

    // Actualizar el texto del botón
    editButton.textContent = isEditingEnabled ? "Deshabilitar Edición" : "Habilitar Edición";
}

// Inicializar la tabla con controles al cargar la página
function initializeTable() {
    initializeRowControls(); // Agregar controles a filas existentes
    enableCellEditing(); // Habilitar edición de celdas
    buildToolbar(); // Barra superior: edición, horas y avionetas

    // desabilitar Edición al cargar la página
    toggleEditMode();

    applyView(); // rango de horas y matrículas guardados
    const scroll = document.querySelector(".table-scroll");
    if (scroll) scroll.classList.remove("is-pending");
}



/* ------------------------------------------------------------------ *
 * Configuración de la tabla: rango de horas y matrículas visibles.
 * Las columnas de hora se identifican por el número de la cabecera y las
 * matrículas por el <th> de cada fila, así vale para HTML antiguos (8-20)
 * y nuevos (0-23). Ocultar es solo visual: los datos siguen en el DOM.
 * ------------------------------------------------------------------ */
const CONFIG_EL = document.getElementById("table-config");
const CONFIG = CONFIG_EL
    ? JSON.parse(CONFIG_EL.textContent)
    : { authenticated: false, preferences: { hour_start: 8, hour_end: 20, hidden_planes: [] } };
const state = {
    hour_start: CONFIG.preferences.hour_start,
    hour_end: CONFIG.preferences.hour_end,
    hidden_planes: (CONFIG.preferences.hidden_planes || []).slice(),
};
let toolbarEls = {};

// hora -> índice de columna, según la cabecera
function hourColumns() {
    const map = new Map();
    Array.from(table.tHead.rows[0].cells).forEach((cell, index) => {
        const text = cell.textContent.trim();
        if (/^\d{1,2}$/.test(text)) map.set(Number(text), index);
    });
    return map;
}

function planeOf(row) {
    const th = row.querySelector("th");
    return th ? th.textContent.trim() : null;
}

function dataRows() {
    return Array.from(table.tBodies[0].rows);
}

function allPlanes() {
    const planes = [];
    dataRows().forEach((row) => {
        const plane = planeOf(row);
        if (plane && !planes.includes(plane)) planes.push(plane);
    });
    return planes;
}

// la hora (tal cual aparece) tiene algún vuelo entre las matrículas visibles
function hoursWithFlights(hiddenPlanes) {
    const columns = hourColumns();
    const hours = new Set();
    dataRows().forEach((row) => {
        if (hiddenPlanes.includes(planeOf(row))) return;
        columns.forEach((index, hour) => {
            const cell = row.cells[index];
            if (cell && cell.textContent.trim() !== "") hours.add(hour);
        });
    });
    return hours;
}

function setHidden(cell, hidden) {
    if (cell) cell.classList.toggle("is-hidden", hidden);
}

function applyView() {
    const columns = hourColumns();
    const rows = [table.tHead.rows[0], ...dataRows()];
    columns.forEach((index, hour) => {
        const hidden = hour < state.hour_start || hour > state.hour_end;
        rows.forEach((row) => setHidden(row.cells[index], hidden));
    });
    dataRows().forEach((row) => {
        const plane = planeOf(row);
        row.classList.toggle("is-hidden", plane !== null && state.hidden_planes.includes(plane));
    });
    refreshHourSelects();
}

/* ---------- guardado ---------- */
function showStatus(message, isError) {
    const el = toolbarEls.status;
    if (!el) return;
    el.textContent = message || "";
    el.classList.toggle("table-tools__status--error", Boolean(isError));
}

// Guarda `next` en la base de datos y, solo si sale bien, lo aplica.
async function savePreferences(next) {
    try {
        const response = await fetch("/table/preferences", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            credentials: "same-origin",
            body: JSON.stringify(next),
        });
        if (!response.ok) {
            let detail = "No se pudo guardar la configuración.";
            try {
                const body = await response.json();
                if (body.errors) detail = Object.values(body.errors).join(" ");
                else if (body.error) detail = body.error;
            } catch (e) { /* respuesta sin JSON */ }
            showStatus(detail, true);
            return false;
        }
        Object.assign(state, next);
        showStatus("");
        applyView();
        return true;
    } catch (e) {
        showStatus("No se pudo guardar la configuración. Revisa la conexión.", true);
        return false;
    }
}

/* ---------- diálogos ---------- */
// Devuelve una promesa con true (aceptar) o false (cancelar / Escape).
function openDialog({ title, bodyNodes, acceptLabel, opener, validate }) {
    return new Promise((resolve) => {
        const dialog = document.createElement("dialog");
        dialog.className = "dialog";
        const titleId = "dialog-title-" + Date.now();
        dialog.setAttribute("aria-labelledby", titleId);

        const heading = document.createElement("h2");
        heading.id = titleId;
        heading.className = "dialog__title";
        heading.textContent = title;
        dialog.appendChild(heading);
        bodyNodes.forEach((node) => dialog.appendChild(node));

        const actions = document.createElement("div");
        actions.className = "dialog__actions";
        const cancel = document.createElement("button");
        cancel.type = "button";
        cancel.className = "btn btn--ghost";
        cancel.textContent = "Cancelar";
        const accept = document.createElement("button");
        accept.type = "button";
        accept.className = "btn";
        accept.textContent = acceptLabel;
        actions.append(cancel, accept);
        dialog.appendChild(actions);

        let result = false;
        const refresh = () => { if (validate) accept.disabled = !validate(); };
        dialog.addEventListener("change", refresh);
        cancel.addEventListener("click", () => dialog.close());
        accept.addEventListener("click", () => { result = true; dialog.close(); });
        dialog.addEventListener("close", () => {
            dialog.remove();
            if (opener) opener.focus();
            resolve(result);
        });

        document.body.appendChild(dialog);
        refresh();
        dialog.showModal();
    });
}

function paragraph(text) {
    const p = document.createElement("p");
    p.textContent = text;
    return p;
}

async function openPlanesDialog(opener) {
    const planes = allPlanes();
    const list = document.createElement("ul");
    list.className = "dialog__list";
    const checks = planes.map((plane) => {
        const li = document.createElement("li");
        const label = document.createElement("label");
        const input = document.createElement("input");
        input.type = "checkbox";
        input.value = plane;
        input.checked = !state.hidden_planes.includes(plane);
        label.append(input, " " + plane);
        li.appendChild(label);
        list.appendChild(li);
        return input;
    });
    const hint = paragraph("Las avionetas marcadas se muestran en la tabla; las desmarcadas se ocultan.");
    const warn = paragraph("Debe quedar al menos una avioneta marcada.");
    warn.className = "dialog__hint";

    const validate = () => {
        const ok = checks.some((c) => c.checked);
        warn.hidden = ok;
        return ok;
    };
    const accepted = await openDialog({
        title: "Avionetas de la tabla",
        bodyNodes: [hint, list, warn],
        acceptLabel: "Aceptar",
        opener,
        validate,
    });
    if (!accepted) return;
    const hidden = checks.filter((c) => !c.checked).map((c) => c.value);
    // las ocultas que no están en esta tabla se conservan (son de otros días)
    const keep = state.hidden_planes.filter((p) => !planes.includes(p));
    await savePreferences({
        hour_start: state.hour_start,
        hour_end: state.hour_end,
        hidden_planes: keep.concat(hidden),
    });
}

/* ---------- horas ---------- */
function presentHours() {
    return Array.from(hourColumns().keys()).sort((a, b) => a - b);
}

function fillHourSelect(select, hours) {
    select.innerHTML = "";
    hours.forEach((hour) => {
        const option = document.createElement("option");
        option.value = String(hour);
        option.textContent = String(hour).padStart(2, "0") + ":00";
        select.appendChild(option);
    });
}

// el selector muestra la hora presente más cercana a la preferencia
function refreshHourSelects() {
    if (!toolbarEls.start) return;
    const hours = presentHours();
    if (hours.length === 0) return;
    const start = hours.find((h) => h >= state.hour_start);
    const end = hours.slice().reverse().find((h) => h <= state.hour_end);
    toolbarEls.start.value = String(start !== undefined ? start : hours[hours.length - 1]);
    toolbarEls.end.value = String(end !== undefined ? end : hours[0]);
}

async function onHoursChange(changed) {
    const select = toolbarEls[changed];
    const next = {
        hour_start: state.hour_start,
        hour_end: state.hour_end,
        hidden_planes: state.hidden_planes.slice(),
    };
    // solo cambia el campo que ha tocado el usuario
    next[changed === "start" ? "hour_start" : "hour_end"] = Number(select.value);

    if (next.hour_start > next.hour_end) {
        showStatus("La hora inicial no puede ser mayor que la hora final.", true);
        refreshHourSelects();
        return;
    }

    const flights = hoursWithFlights(next.hidden_planes);
    const before = Array.from(flights).filter((h) => h < next.hour_start);
    const after = Array.from(flights).filter((h) => h > next.hour_end);
    if (before.length || after.length) {
        const parts = [];
        if (before.length) parts.push("anteriores a las " + String(next.hour_start).padStart(2, "0") + ":00");
        if (after.length) parts.push("posteriores a las " + String(next.hour_end).padStart(2, "0") + ":59");
        const accepted = await openDialog({
            title: "Hay vuelos fuera del rango",
            bodyNodes: [paragraph(
                "Hay vuelos " + parts.join(" y ") + ". ¿Seguro que no quieres verlos?")],
            acceptLabel: "Aceptar",
            opener: select,
        });
        if (!accepted) {
            showStatus("");
            refreshHourSelects();
            return;
        }
    }
    const ok = await savePreferences(next);
    if (!ok) refreshHourSelects();
}

/* ---------- barra de herramientas ---------- */
function buildToolbar() {
    const bar = document.createElement("div");
    bar.className = "table-tools";
    bar.setAttribute("role", "toolbar");
    bar.setAttribute("aria-label", "Herramientas de la tabla");

    const editButton = document.createElement("button");
    editButton.type = "button";
    editButton.id = "edit-btn";
    editButton.className = "btn btn--ghost no-edit";
    editButton.textContent = "Deshabilitar Edición";
    editButton.addEventListener("click", toggleEditMode);
    bar.appendChild(editButton);

    if (CONFIG.authenticated) {
        const hours = presentHours();
        const group = document.createElement("div");
        group.className = "table-tools__hours";
        const makeField = (id, text) => {
            const label = document.createElement("label");
            label.className = "table-tools__field";
            label.htmlFor = id;
            const span = document.createElement("span");
            span.textContent = text;
            const select = document.createElement("select");
            select.id = id;
            select.className = "table-tools__select";
            fillHourSelect(select, hours);
            label.append(span, select);
            group.appendChild(label);
            return select;
        };
        toolbarEls.start = makeField("hour-start", "Desde");
        toolbarEls.end = makeField("hour-end", "Hasta");
        toolbarEls.start.addEventListener("change", () => onHoursChange("start"));
        toolbarEls.end.addEventListener("change", () => onHoursChange("end"));
        bar.appendChild(group);

        const planesButton = document.createElement("button");
        planesButton.type = "button";
        planesButton.className = "btn btn--ghost no-edit";
        planesButton.textContent = "Avionetas";
        planesButton.addEventListener("click", () => openPlanesDialog(planesButton));
        bar.appendChild(planesButton);
    }

    const status = document.createElement("p");
    status.className = "table-tools__status";
    status.setAttribute("role", "status");
    toolbarEls.status = status;
    bar.appendChild(status);

    const scroll = document.querySelector(".table-scroll");
    scroll.parentNode.insertBefore(bar, scroll);
}

// Llamar a la función para inicializar la tabla (al final: usa las constantes de arriba)
initializeTable();
