// para /vuelos

function loadingVuelos() {
    const vuelosForm = document.getElementById('vuelosForm');
    const loading = document.getElementById('loading');

    vuelosForm.addEventListener('submit', function () {
        loading.classList.remove('hidden');
    });
}

document.addEventListener('DOMContentLoaded', loadingVuelos);