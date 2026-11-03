/* RISHINE · CUENTAS · Validación de formularios (iniciar sesión, crear cuenta
   de usuario y crear cuenta de promotor)
   Archivo : cuentas/static/cuentas/js/cuentas_formularios.js
   Reemplaza a crear_cuenta.js: ahora jala en las tres pantallas.

   QUÉ HACE
   1. Valida los formularios con mensajes que dicen CÓMO corregir:
      al salir de un campo, al corregirlo y al enviar. Al fallar, lleva el
      foco al primer campo con error.
   2. Activa los botones "Mostrar / Ocultar" de las contraseñas.

   CÓMO SE ACTIVA
   Cualquier <form data-cuenta-form> se inicia solo al cargar la página.
   Si el formulario aparece después (lo inserta cuentas_modal.js dentro de la
   ventana emergente) se inicia llamando:
       RishineCuentasFormularios.iniciar(contenedor);
   Iniciar dos veces el mismo formulario es seguro (se marca con
   data-iniciado).

   QUÉ NO HACE
   Es ayuda para la persona, no seguridad. La validación real (correo
   repetido, contraseña, edad, tipo de archivo) debe repetirse en la vista de
   Django, que devolverá `errores` al template.

   SIN JAVASCRIPT
   Los formularios siguen funcionando: el navegador valida con required,
   type y minlength, y el botón "Mostrar" permanece oculto.

   CÓMO AGREGAR UN CAMPO
   Pon un <input name="x" id="x"> con su <p id="error-x" hidden> y, si
   necesita una regla propia, agrégala en `reglas` (abajo). Un campo sin regla
   propia usa la validación nativa del navegador (required, type, minlength). */

(function () {
    'use strict';

    /* Configuración (edita aquí; no hay números sueltos más abajo) */
    var MIN_CONTRASENA = 8;                 // debe coincidir con minlength del HTML
    var MIN_EDAD = 15;                      // Rishine es para personas de 15 a 29 años
    var MAX_EDAD = null;                    // 29 para bloquear mayores; null = sin tope
    var MAX_MB_ARCHIVO = 5;                 // tamaño máximo del INE
    var TIPOS_ARCHIVO = /^(image\/.+|application\/pdf)$/;

    /* Utilidades */

    /** Busca un elemento por id dentro del formulario. */
    function dentro(form, id) {
        return form.querySelector('[id="' + id + '"]');
    }

    /** Años cumplidos hoy, a partir de 'AAAA-MM-DD'. */
    function calcularEdad(iso) {
        var p = iso.split('-');
        if (p.length !== 3) { return NaN; }
        var hoy = new Date();
        var edad = hoy.getFullYear() - Number(p[0]);
        var m = hoy.getMonth() + 1 - Number(p[1]);
        if (m < 0 || (m === 0 && hoy.getDate() < Number(p[2]))) { edad--; }
        return edad;
    }

    /* Reglas por nombre de campo 
       Cada regla recibe (valor, campo, form) y devuelve '' si está bien o el
       mensaje de error. Los mensajes explican cómo corregir. */
    var reglas = {
        /* Iniciar sesión */
        username: function (v) {
            return v.trim() ? '' : 'Escribe tu nombre de usuario.';
        },
        password: function (v) {
            return v ? '' : 'Escribe tu contraseña.';
        },

        /* Crear cuenta (usuario y promotor) */
        nombre: function (v) {
            return v.trim() ? '' : 'Escribe tu nombre.';
        },
        apellidos: function (v) {
            return v.trim() ? '' : 'Escribe tus apellidos.';
        },
        correo: function (v) {
            v = v.trim();
            if (!v) { return 'Escribe tu correo electrónico.'; }
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)
                ? '' : 'Revisa tu correo. Debe verse así: nombre@ejemplo.com.';
        },
        fecha_nacimiento: function (v) {
            if (!v) { return 'Elige tu fecha de nacimiento.'; }
            var edad = calcularEdad(v);
            if (isNaN(edad) || edad < 0) { return 'Elige una fecha que ya haya pasado.'; }
            if (edad < MIN_EDAD) {
                return 'Necesitas tener al menos ' + MIN_EDAD + ' años para crear una cuenta.';
            }
            if (MAX_EDAD !== null && edad > MAX_EDAD) {
                return 'Rishine es para personas de ' + MIN_EDAD + ' a ' + MAX_EDAD + ' años.';
            }
            return '';
        },
        contrasena: function (v) {
            if (!v) { return 'Crea una contraseña.'; }
            return v.length >= MIN_CONTRASENA
                ? '' : 'Usa al menos ' + MIN_CONTRASENA + ' caracteres. Ahora tienes ' + v.length + '.';
        },
        contrasena2: function (v, _campo, form) {
            if (!v) { return 'Escribe tu contraseña otra vez.'; }
            var original = form.elements.contrasena;
            return original && v === original.value
                ? '' : 'Las contraseñas no coinciden. Escribe la misma en los dos campos.';
        },
        terminos: function (_v, campo) {
            return campo.checked
                ? '' : 'Marca la casilla para aceptar los términos y crear tu cuenta.';
        },

        /* Solo promotor */
        organizacion: function (v) {
            return v.trim() ? '' : 'Escribe el nombre de tu organización.';
        }
    };

    /* Mostrar / ocultar el error de un campo */
    function pintar(form, campo, mensaje) {
        var caja = dentro(form, 'error-' + campo.id);
        if (mensaje) {
            campo.setAttribute('aria-invalid', 'true');
            campo.classList.add('is-invalid');
            if (caja) { caja.textContent = mensaje; caja.hidden = false; }
        } else {
            campo.removeAttribute('aria-invalid');
            campo.classList.remove('is-invalid');
            if (caja) { caja.textContent = ''; caja.hidden = true; }
        }
        return !mensaje;
    }

    /** Valida un campo; devuelve true si está bien. */
    function validar(form, campo) {
        var regla = reglas[campo.name];
        var mensaje = regla
            ? regla(campo.value, campo, form)
            : (campo.checkValidity() ? '' : campo.validationMessage);   // sin regla propia
        return pintar(form, campo, mensaje);
    }

    /* Inicio de un formulario */
    function iniciarFormulario(form) {
        if (form.getAttribute('data-iniciado')) { return; }
        form.setAttribute('data-iniciado', 'true');

        /* Desactiva los globos nativos: los mensajes salen de este script.
           (Si el script no carga, esta línea no corre y el navegador valida.) */
        form.noValidate = true;

        var campos = Array.prototype.slice.call(
            form.querySelectorAll('input[name]:not([type="hidden"])')
        );

        campos.forEach(function (campo) {
            var evento = (campo.type === 'checkbox' || campo.type === 'file') ? 'change' : 'input';

            // Al salir del campo: valida por primera vez, pero con dos cuidados.
            //  - Un campo vacío no se regaña al salir: eso se avisa al enviar.
            //  - Si el foco se va a algo fuera del formulario (un enlace, la X de
            //    la ventana), no se valida: el mensaje nuevo empujaría el
            //    contenido hacia abajo y el clic caería en otro lado.
            campo.addEventListener('blur', function (e) {
                if (campo.type === 'checkbox' || campo.type === 'file') { return; }
                if (e.relatedTarget && !form.contains(e.relatedTarget)) { return; }
                if (campo.value || campo.getAttribute('aria-invalid') === 'true') {
                    validar(form, campo);
                }
            });

            // Mientras escribe: solo revalida si ya mostraba error (no regañar antes).
            campo.addEventListener(evento, function () {
                if (campo.type === 'file' || campo.getAttribute('aria-invalid') === 'true') {
                    validar(form, campo);
                }
                // Si cambia la contraseña y ya hay confirmación, comparar de nuevo.
                if (campo.name === 'contrasena' && form.elements.contrasena2 &&
                    form.elements.contrasena2.value) {
                    validar(form, form.elements.contrasena2);
                }
            });
        });

        // Al enviar: valida todo y detiene el envío si algo falla.
        // (cuentas_modal.js también escucha este evento y respeta preventDefault.)
        form.addEventListener('submit', function (e) {
            var primero = null;
            campos.forEach(function (campo) {
                if (!validar(form, campo) && !primero) { primero = campo; }
            });
            if (primero) {
                e.preventDefault();
                primero.focus();
            }
        });

        // Botones Mostrar / Ocultar contraseña.
        Array.prototype.forEach.call(
            form.querySelectorAll('[data-mostrar-contrasena]'),
            function (boton) {
                var input = dentro(form, boton.getAttribute('data-mostrar-contrasena'));
                if (!input) { return; }
                boton.hidden = false;   // sin JS permanece oculto: no hay botón muerto
                boton.addEventListener('click', function () {
                    var visible = input.type === 'text';
                    input.type = visible ? 'password' : 'text';
                    boton.textContent = visible ? 'Mostrar' : 'Ocultar';
                    boton.setAttribute('aria-pressed', String(!visible));
                    input.focus();
                });
            }
        );
    }

    /** Inicia todos los <form data-cuenta-form> dentro de `raiz`. */
    function iniciar(raiz) {
        Array.prototype.forEach.call(
            (raiz || document).querySelectorAll('form[data-cuenta-form]'),
            iniciarFormulario
        );
    }

    window.RishineCuentasFormularios = { iniciar: iniciar };

    // Inicio automático (también si el script se carga tarde, p. ej. desde el modal).
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { iniciar(); });
    } else {
        iniciar();
    }
})();
