const modo = document.getElementById('modo');


modo.addEventListener('change', function() {
    const direccion = document.querySelectorAll('.direccion');
    const referencias = document.querySelectorAll('.referencias');
    const url_evento = document.querySelectorAll('.url_evento');
    if (this.value === 'Virtual') {
        direccion.forEach(el => el.style.display = 'none');
        referencias.forEach(el => el.style.display = 'none');
        url_evento.forEach(el => el.style.display = 'block');
    } else if (this.value === 'Presencial') {
        direccion.forEach(el => el.style.display = 'block');
        referencias.forEach(el => el.style.display = 'block');
        url_evento.forEach(el => el.style.display = 'none');
    } else {
        direccion.forEach(el => el.style.display = 'block');
        referencias.forEach(el => el.style.display = 'block');
        url_evento.forEach(el => el.style.display = 'block');
    }
});

function eventoDias(radio) {
    if (radio.value === 'un_dia') {
        document.querySelectorAll('.fecha_inicio').forEach(el => el.style.display = 'block');
        document.querySelectorAll('.fecha_fin').forEach(el => el.style.display = 'none');
    } else if (radio.value === 'varios_dias') {
        document.querySelectorAll('.fecha_inicio').forEach(el => el.style.display = 'block');
        document.querySelectorAll('.fecha_fin').forEach(el => el.style.display = 'block');
    }
}