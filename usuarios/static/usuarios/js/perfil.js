(function () {
    const btnEditar = document.getElementById('btn-modificar-perfil');
    const btnGuardar = document.getElementById('btn-guardar-perfil');
    const campos = [
        document.getElementById('nombreUsuario'),
        document.getElementById('nombre'),
        document.getElementById('apellido'),
        document.getElementById('correo'),
        document.getElementById('ciudad'),
        document.getElementById('fecha_de_nacimiento')
    ];

    if (!btnEditar || !btnGuardar) return;

    let editable = false;
    btnGuardar.disabled = true;

    btnEditar.addEventListener('click', function (e) {
        e.preventDefault();
        editable = !editable;
        campos.forEach(function (campo) {
            if (!campo) return;
            campo.readOnly = !editable;
        });

        btnGuardar.disabled = !editable;
        btnEditar.classList.toggle('activo', editable);
        btnEditar.textContent = editable ? 'Cancelar' : 'Modificar';

        if (editable && campos[0]) {
            campos[0].focus();
        }
    });

})();