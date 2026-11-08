const modo = document.getElementById('modo');

function mostrar(selector, visible) {
    document.querySelectorAll(selector).forEach(function (el) {
        el.style.display = visible ? 'block' : 'none';
    });
}

function actualizarModo() {
    const m = modo.value;
    mostrar('.direccion', m !== 'virtual');
    mostrar('.referencias', m !== 'virtual');
    mostrar('.url_evento', m !== 'presencial');
}

function eventoDias(radio) {
    mostrar('.fecha_inicio', true);
    mostrar('.fecha_fin', radio.value === 'varios_dias');
}

modo.addEventListener('change', actualizarModo);
actualizarModo();