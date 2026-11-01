/* RISHINE · CUENTAS · Ventana emergente (modal) para las tres pantallas:
   iniciar sesión · crear cuenta de usuario · crear cuenta de promotor
   
   Archivo : cuentas/static/cuentas/js/cuentas_modal.js
   Estilos : cuentas/static/cuentas/css/cuentas_modal.css (los carga este script)

   QUÉ HACE
   Abre cualquiera de las tres pantallas encima de la página en la que está la
   persona, como una ventana emergente, sin recargar. Las propias pantallas
   (templates de Django) NO cambian: el script pide la página con fetch(),
   toma su bloque `.cuenta` y lo coloca dentro de un <dialog>.

   - Un solo <dialog> reutilizado. El contenido cambia entre las tres
     pantallas (de "Iniciar sesión" a "Crear cuenta", etc.) sin cerrarlo.
   - Los formularios se envían con fetch() (FormData, incluye el archivo del
     INE). Si el servidor responde con la misma pantalla (errores, mensajes)
     se vuelve a pintar dentro de la ventana. Si responde con una redirección
     a otra página (cuenta creada, sesión iniciada) se navega a ella.
   - Se cierra con la X, con Esc o al hacer clic fuera de la ventana.
   - Foco: al abrir va al primer campo; al cerrar regresa al enlace que la
     abrió. El resto de la página queda inerte mientras está abierta
     (lo hace <dialog>.showModal()).

   CÓMO SE ACTIVA (2 pasos)
   1) En templates/base.html, antes de </body>:
        <script src="{% static 'cuentas/js/cuentas_modal.js' %}"
                data-css="{% static 'cuentas/css/cuentas_modal.css' %}"
                defer></script>
   2) Marca con data-cuenta-modal cada enlace que deba abrir la ventana,
      sin quitarle su href (es el respaldo si no hay JavaScript):
        <a href="{% url 'cuentas:login' %}" data-cuenta-modal>Iniciar sesión</a>
        <a href="{% url 'cuentas:registro' %}" data-cuenta-modal>Crear cuenta</a>
        <a href="{% url 'cuentas:registro_promotor' %}" data-cuenta-modal>…</a>

   ABRIR DESDE OTRO JAVASCRIPT
        RishineCuentasModal.abrir('/cuentas/login/');
        RishineCuentasModal.cerrar();

   QUÉ NO SE ROMPE
   - Sin JavaScript (o en un navegador sin <dialog>) los enlaces navegan a la
     pantalla completa de siempre.
   - En las propias pantallas de cuenta (/cuentas/login/, etc.) los enlaces
     NO abren ventana: navegan normal, para no apilar una ventana sobre una
     página que ya es el formulario.
   - Ctrl/Cmd/Shift+clic y clic central abren en pestaña nueva como siempre.

   LO QUE NECESITA DEL SERVIDOR
   Nada nuevo: las vistas actuales sirven. Al abrir desde otra página se agrega
   ?next=<página actual> a la URL pedida, para que el login regrese ahí
   (inicio_sesion.html ya lee request.GET.next).
   Importante: una vista de login/registro exitoso debe responder con un
   redirect (HTTP 302), como es costumbre en Django.

   ÍNDICE DEL ARCHIVO para encontrar cosas rápido :V
   1. Configuración
   2. Estado y creación de la ventana
   3. Pedir páginas y cargar sus recursos (CSS/JS)
   4. Pintar el contenido recibido
   5. Abrir y cerrar
   6. Eventos (enlaces, formularios, Esc, clic fuera)
   7. API pública */

(function () {
    'use strict';

    /* Si ya se cargó, o el navegador no soporta <dialog>, no se hace nada y
       los enlaces siguen navegando a la pantalla completa. */
    if (window.RishineCuentasModal) { return; }
    var pruebaDialog = document.createElement('dialog');
    if (typeof pruebaDialog.showModal !== 'function') { return; }

    var scriptPropio = document.currentScript;

    /* 1 CONFIGURACIÓN */
    var SELECTOR_ENLACE = 'a[data-cuenta-modal]';   // enlaces que abren la ventana
    var SELECTOR_CONTENIDO = '.cuenta';             // bloque que se toma de cada página
    var DURACION = 180;                             // ms; igual que --duracion del CSS
    var TEXTO_CARGANDO = 'Cargando…';
    var TEXTO_FALLO = 'No pudimos conectar. Revisa tu conexión e inténtalo de nuevo.';

    /* 2 ESTADO Y CREACIÓN DE LA VENTANA */
    var dialogo = null;         // <dialog>, se crea la primera vez
    var contenido = null;       // zona donde se pinta la pantalla de cuenta
    var abridor = null;         // elemento que tenía el foco al abrir
    var urlActual = '';         // URL de la pantalla mostrada (destino por defecto de los forms)
    var next = '';              // adónde volver tras iniciar sesión
    var solicitud = 0;          // contador para ignorar respuestas viejas
    var cerrando = false;

    function reduceMovimiento() {
        return window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    /** Carga la hoja de estilos de la ventana (una sola vez). */
    function cargarEstilosPropios() {
        var href = scriptPropio && scriptPropio.getAttribute('data-css');
        if (!href && scriptPropio && scriptPropio.src) {
            href = scriptPropio.src.replace('/js/cuentas_modal.js', '/css/cuentas_modal.css');
        }
        if (!href || existeRecurso('link[rel="stylesheet"]', 'href', href)) { return; }
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        document.head.appendChild(link);
    }

    /** Crea el <dialog> la primera vez que se necesita. */
    function crearDialogo() {
        if (dialogo) { return; }
        cargarEstilosPropios();

        dialogo = document.createElement('dialog');
        dialogo.className = 'cuenta-modal';
        dialogo.setAttribute('aria-label', 'Cuenta');
        dialogo.innerHTML =
            '<div class="cuenta-modal__ventana">' +
              '<button type="button" class="cuenta-modal__cerrar" aria-label="Cerrar ventana">' +
                /* Ícono de trazo a 20px, como los del navbar */
                '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" ' +
                     'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
                  '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>' +
                '</svg>' +
              '</button>' +
              '<div class="cuenta-modal__contenido"></div>' +
            '</div>';
        document.body.appendChild(dialogo);
        contenido = dialogo.querySelector('.cuenta-modal__contenido');

        /* X de cerrar */
        dialogo.querySelector('.cuenta-modal__cerrar').addEventListener('click', cerrar);

        /* Esc: <dialog> dispara "cancel"; lo cambiamos por nuestro cierre animado */
        dialogo.addEventListener('cancel', function (e) { e.preventDefault(); cerrar(); });

        /* Clic fuera de la ventana. Se exige que el clic EMPIECE y TERMINE en
           el fondo, para que arrastrar para seleccionar texto no la cierre. */
        var empezoFuera = false;
        dialogo.addEventListener('mousedown', function (e) { empezoFuera = (e.target === dialogo); });
        dialogo.addEventListener('click', function (e) {
            if (e.target === dialogo && empezoFuera) { cerrar(); }
        });

        /* Enlaces y formularios que vienen DENTRO de la ventana */
        dialogo.addEventListener('click', alHacerClicEnVentana);
        dialogo.addEventListener('submit', alEnviarFormulario);
    }

    /*  3 PEDIR PÁGINAS Y CARGAR SUS RECURSOS */

    /** ¿Ya existe en el documento un <link>/<script> con esa URL? */
    function existeRecurso(selector, atributo, urlAbsoluta) {
        var lista = document.querySelectorAll(selector);
        for (var i = 0; i < lista.length; i++) {
            if (lista[i][atributo] === new URL(urlAbsoluta, location.href).href) { return true; }
        }
        return false;
    }

    /** fetch con las cabeceras comunes. */
    function pedir(url, opciones) {
        opciones = opciones || {};
        opciones.credentials = 'same-origin';
        opciones.headers = {
            'X-Requested-With': 'XMLHttpRequest',   // permite a la vista distinguirla si quiere
            'Accept': 'text/html'
        };
        return fetch(url, opciones);
    }

    /** Agrega ?next=… a la URL (solo si hay un destino y la URL no lo trae). */
    function conNext(url) {
        var u = new URL(url, location.href);
        if (next && !u.searchParams.has('next')) { u.searchParams.set('next', next); }
        return u.href;
    }

    /** Carga los <link rel=stylesheet> y <script src> de la página recibida
        que todavía no estén en el documento. Devuelve una promesa. */
    function cargarRecursos(doc, base) {
        var promesas = [];

        Array.prototype.forEach.call(doc.querySelectorAll('link[rel="stylesheet"]'), function (l) {
            var href = new URL(l.getAttribute('href'), base).href;
            if (existeRecurso('link[rel="stylesheet"]', 'href', href)) { return; }
            promesas.push(new Promise(function (ok) {
                var nuevo = document.createElement('link');
                nuevo.rel = 'stylesheet';
                nuevo.href = href;
                nuevo.onload = nuevo.onerror = ok;      // un CSS que falla no debe bloquear
                document.head.appendChild(nuevo);
            }));
        });

        Array.prototype.forEach.call(doc.querySelectorAll('script[src]'), function (s) {
            var src = new URL(s.getAttribute('src'), base).href;
            if (scriptPropio && src === scriptPropio.src) { return; }   // este mismo archivo
            if (existeRecurso('script[src]', 'src', src)) { return; }
            promesas.push(new Promise(function (ok) {
                var nuevo = document.createElement('script');
                nuevo.src = src;
                nuevo.onload = nuevo.onerror = ok;
                document.body.appendChild(nuevo);
            }));
        });

        return Promise.all(promesas);
    }

    /* 4 PINTAR EL CONTENIDO RECIBIDO */

    function mostrarCargando() {
        contenido.innerHTML = '';
        var p = document.createElement('p');
        p.className = 'text-base cuenta-modal__cargando';
        p.setAttribute('role', 'status');
        p.textContent = TEXTO_CARGANDO;
        contenido.appendChild(p);
        dialogo.setAttribute('aria-busy', 'true');
    }

    /** Alerta de fallo de red, con el formato de alertas de la guía. */
    function mostrarFallo() {
        var aviso = document.createElement('div');
        aviso.className = 'alerta alerta--error cuenta-modal__fallo';
        aviso.setAttribute('role', 'alert');
        aviso.innerHTML = '<strong>Error.</strong> ';
        aviso.appendChild(document.createTextNode(TEXTO_FALLO));

        var cuenta = contenido.querySelector(SELECTOR_CONTENIDO);
        var anterior = contenido.querySelector('.cuenta-modal__fallo');
        if (anterior) { anterior.remove(); }
        if (cuenta) { cuenta.insertBefore(aviso, cuenta.firstChild); }
        else { contenido.innerHTML = ''; contenido.appendChild(aviso); }

        var boton = contenido.querySelector('button[type="submit"]');
        if (boton) { boton.disabled = false; }
        dialogo.removeAttribute('aria-busy');
    }

    /** Pinta la pantalla de cuenta contenida en `doc`. */
    function pintar(doc, urlFinal) {
        var origen = doc.querySelector(SELECTOR_CONTENIDO);
        var tarea = cargarRecursos(doc, urlFinal);

        return tarea.then(function () {
            contenido.innerHTML = '';
            contenido.appendChild(document.importNode(origen, true));
            urlActual = urlFinal;

            /* El título de la pantalla nombra la ventana (lectores de pantalla) */
            var h1 = contenido.querySelector('h1');
            if (h1) {
                h1.id = 'cuenta-modal-titulo';
                dialogo.setAttribute('aria-labelledby', 'cuenta-modal-titulo');
                dialogo.removeAttribute('aria-label');
            }

            /* Activa validación y botón "Mostrar" en el formulario recién pintado */
            if (window.RishineCuentasFormularios) {
                window.RishineCuentasFormularios.iniciar(contenido);
            }

            dialogo.removeAttribute('aria-busy');
            enfocarPrimerCampo();
        });
    }

    /** Foco al primer campo con error o, si no hay, al primer campo. */
    function enfocarPrimerCampo() {
        var campo = contenido.querySelector('[aria-invalid="true"], .is-invalid') ||
                    contenido.querySelector('input:not([type="hidden"]), button[type="submit"]');
        if (campo) { campo.focus(); }
    }

    /** Procesa una respuesta del servidor. */
    function procesarRespuesta(resp, miSolicitud) {
        return resp.text().then(function (html) {
            if (miSolicitud !== solicitud) { return; }          // llegó tarde: se ignora

            var doc = new DOMParser().parseFromString(html, 'text/html');
            if (doc.querySelector(SELECTOR_CONTENIDO)) {
                return pintar(doc, resp.url);                    // sigue siendo una pantalla de cuenta
            }
            if (resp.redirected || resp.ok) {
                /* Fue a otra página (p. ej. inicio tras iniciar sesión): se
                   navega a ella. Los mensajes de Django se conservan porque
                   esa página aún no los mostró. */
                window.location.assign(resp.url);
                return;
            }
            mostrarFallo();                                      // 4xx/5xx sin pantalla de cuenta
        });
    }

    /* 5 ABRIR Y CERRAR */

    /** Pide `url` (GET) y la pinta dentro de la ventana. */
    function cargar(url) {
        var miSolicitud = ++solicitud;
        mostrarCargando();
        return pedir(conNext(url))
            .then(function (resp) { return procesarRespuesta(resp, miSolicitud); })
            .catch(function () { if (miSolicitud === solicitud) { mostrarFallo(); } });
    }

    /** Abre la ventana mostrando la pantalla de `url`. */
    function abrir(url, elementoAbridor) {
        crearDialogo();
        if (!dialogo.open) {
            abridor = elementoAbridor || document.activeElement;
            /* Primera apertura desde una página normal: recuerda dónde estaba */
            next = location.pathname + location.search;
            cerrando = false;
            dialogo.showModal();
            document.documentElement.classList.add('cuenta-modal-abierto');
            /* Un fotograma después, para que la transición de entrada se vea */
            requestAnimationFrame(function () { dialogo.classList.add('is-abierto'); });
        }
        return cargar(url);
    }

    /** Cierra la ventana con su transición de salida. */
    function cerrar() {
        if (!dialogo || !dialogo.open || cerrando) { return; }
        cerrando = true;
        solicitud++;                                             // cancela respuestas pendientes
        dialogo.classList.remove('is-abierto');

        function terminar() {
            dialogo.close();
            contenido.innerHTML = '';
            document.documentElement.classList.remove('cuenta-modal-abierto');
            cerrando = false;
            if (abridor && document.contains(abridor) && abridor.focus) { abridor.focus(); }
            abridor = null;
        }
        if (reduceMovimiento()) { terminar(); } else { setTimeout(terminar, DURACION); }
    }

    /* 6 EVENTOS */

    /** ¿Estamos en una página que YA es una pantalla de cuenta completa? */
    function esPaginaDeCuenta() {
        return !!document.querySelector('main ' + SELECTOR_CONTENIDO);
    }

    /** Enlaces marcados con data-cuenta-modal fuera de la ventana. */
    document.addEventListener('click', function (e) {
        if (e.defaultPrevented || e.button !== 0 ||
            e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) { return; }
        var enlace = e.target.closest && e.target.closest(SELECTOR_ENLACE);
        if (!enlace || (dialogo && dialogo.contains(enlace))) { return; }
        if (esPaginaDeCuenta()) { return; }                      // navega normal
        e.preventDefault();
        abrir(enlace.href, enlace);
    });

    /** Enlaces marcados que están DENTRO de la ventana: cambian de pantalla. */
    function alHacerClicEnVentana(e) {
        var enlace = e.target.closest && e.target.closest(SELECTOR_ENLACE);
        if (!enlace || e.button !== 0 ||
            e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) { return; }
        e.preventDefault();
        cargar(enlace.href);
    }

    /** Envío de formularios dentro de la ventana. */
    function alEnviarFormulario(e) {
        if (e.defaultPrevented) { return; }          // la validación de cuentas_formularios.js ya lo frenó
        var form = e.target;
        e.preventDefault();

        var miSolicitud = ++solicitud;
        var boton = e.submitter || form.querySelector('button[type="submit"]');
        if (boton) { boton.disabled = true; }        // evita doble envío
        dialogo.setAttribute('aria-busy', 'true');

        /* action="" significa "esta misma URL": aquí, la de la pantalla mostrada */
        var destino = form.getAttribute('action') || urlActual;

        pedir(destino, { method: (form.method || 'post').toUpperCase(), body: new FormData(form) })
            .then(function (resp) { return procesarRespuesta(resp, miSolicitud); })
            .catch(function () { if (miSolicitud === solicitud) { mostrarFallo(); } });
    }

    /* 7 API PÚBLICA */
    window.RishineCuentasModal = { abrir: abrir, cerrar: cerrar };
})();
