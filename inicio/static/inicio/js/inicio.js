var secciones = document.querySelectorAll('.bienvenido, .seccion-para-ti, .seccion-menos-de-500, .seccion-menos-de-200, .banner-cta');

for (var i = 0; i < secciones.length; i++) {
    secciones[i].classList.add('escondido');
}

function mostrarSecciones() {
    for (var i = 0; i < secciones.length; i++) {
        var posicion = secciones[i].getBoundingClientRect().top;

        if (posicion < window.innerHeight - 50) {
            secciones[i].classList.add('aparece');
        }
    }
}

window.addEventListener('scroll', mostrarSecciones);
setTimeout(mostrarSecciones, 100);