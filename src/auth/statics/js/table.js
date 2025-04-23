const table = document.querySelector(".dataframe");

// Función para agregar botones de control a cada fila
function addRowControls(row) {
    const controlCell = document.createElement("td");
    controlCell.classList.add("control-buttons", "no-edit"); // Clase para identificar la columna no editable
    controlCell.innerHTML = `
        <button onclick="addRowBelow(this)">➕ Fila Abajo</button>
        <button onclick="deleteSpecificRow(this)">❌ Eliminar Fila</button>
    `;
    row.insertBefore(controlCell, row.firstChild);
}

// Función para inicializar los controles en filas existentes
function initializeRowControls() {
    const rows = table.querySelectorAll("tbody tr");
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
    const cells = table.querySelectorAll("tbody td");

    // Alternar visibilidad de los botones de control
    controlButtons.forEach((buttonCell) => {
        buttonCell.style.display = buttonCell.style.display === "none" ? "" : "none";
    });

    // Alternar entre habilitar/deshabilitar edición
    cells.forEach((cell) => {
        if (cell.classList.contains("no-edit")) return; // No editar las celdas de control
        if (cell.isContentEditable) {
            cell.contentEditable = "false"; // Deshabilitar edición
        } else {
            cell.contentEditable = "true"; // Habilitar edición
        }
    });
}

// Función para agregar el botón de "Habilitar Edición" al final de la tabla
function addToggleEditButton() {
    const toggleButtonRow = document.createElement("tr");
    const toggleButtonCell = document.createElement("td");
    toggleButtonCell.colSpan = table.rows[0].cells.length; // Ocupa todo el ancho de la tabla
    toggleButtonCell.style.textAlign = "center";

    toggleButtonCell.innerHTML = `
        <button onclick="toggleEditMode()">Habilitar Edición</button>
    `;
    toggleButtonRow.appendChild(toggleButtonCell);
    table.querySelector("tbody").appendChild(toggleButtonRow);
}

// Inicializar la tabla con controles al cargar la página
function initializeTable() {
    initializeRowControls(); // Agregar controles a filas existentes
    enableCellEditing(); // Habilitar edición de celdas
    addToggleEditButton(); // Agregar el botón de "Habilitar Edición"
}

// Llamar a la función para inicializar la tabla
initializeTable();