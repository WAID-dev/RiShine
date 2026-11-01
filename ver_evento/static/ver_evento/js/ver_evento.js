//ANIMACION DE APARICION

const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.classList.add('visible');
            observer.unobserve(e.target);
        }
    });
}, { threshold: 0.15 });

document.querySelectorAll(
    '#tituloEimagen, #fecha, #dias, #cupo, #costo, #ubicacion, #seccionDescripcion'
).forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
});