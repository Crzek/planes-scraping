// para /vuelos

 document.addEventListener('DOMContentLoaded', function () {
        const vuelosForm = document.getElementById('vuelosForm');
        const remakeForm = document.getElementById('remakeForm');
        const loading = document.getElementById('loading');
        const containerForm = document.getElementById('container-form');

        if (vuelosForm) {
            vuelosForm.addEventListener('submit', function () {
                loading.classList.remove('hidden');
                containerForm.classList.add('hidden');
            });
        }

        if (remakeForm) {
            remakeForm.addEventListener('submit', function () {
                loading.classList.remove('hidden');
                containerForm.classList.add('hidden');
            });
        }
    });