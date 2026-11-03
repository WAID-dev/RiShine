/*
* Activa y desactiva la edición de los campos del formulario.
* El btn modificar habilita los campos y al botón Guardar.
* El boton Cancelar los bloquea de nuevo y restaura los valores originales.
* */
(function () {
    const btnEditar = document.getElementById('btn-modificar-perfil');
    const btnGuardar = document.getElementById('btn-guardar-perfil');
    // Campos del formulario que se pueden editar
    const campos = [
        document.getElementById('nombreUsuario'),
        document.getElementById('nombre'),
        document.getElementById('apellido'),
        document.getElementById('correo'),
        document.getElementById('ciudad'),
        document.getElementById('fecha_de_nacimiento')
    ];

    // Si la página no tiene los botones, no hace nada
    if (!btnEditar || !btnGuardar) return;

    // Copia de los valores que llegaron del servidor, para poder restaurarlos al cancelar
    const originales = campos.map(function (c) { return c ? c.value : ''; });


    let editable = false; // false = solo lectura, true = editando
    btnGuardar.disabled = true; // no se puede guardar hasta presionar "Modificar

    btnEditar.addEventListener('click', function (e) {
        e.preventDefault();  // el botón no debe enviar el formulario
        editable = !editable; // alterna entre editar y cancelar
        campos.forEach(function (campo, i) {
            if (!campo) return;
            campo.readOnly = !editable;
            // Al cancelar, se descartan los cambios escritos
            if (!editable) campo.value = originales[i];
        });

        // Actualiza el aspecto y texto de los botones según el modo
        btnGuardar.disabled = !editable;
        btnEditar.classList.toggle('activo', editable);
        btnEditar.textContent = editable ? 'Cancelar' : 'Modificar';

         // Al empezar a editar, el cursor va al primer campo
        if (editable && campos[0]) {
            campos[0].focus();
        }
    });

})();