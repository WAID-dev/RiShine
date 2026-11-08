from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import RegistroPromotorForm, RegistroUsuarioForm, errores_a_dict
from usuarios.models import Promotor

User = get_user_model()

# Campos que se devuelven a la plantilla para no perderlos si hay un error.
# Las contraseñas nunca se devuelven.
CAMPOS_USUARIO = ('nombre', 'apellidos', 'username', 'correo', 'fecha_nacimiento', 'ciudad')
CAMPOS_PROMOTOR = ('nombre', 'apellidos', 'username', 'correo', 'organizacion')

USUARIO_REPETIDO = 'Ese nombre de usuario ya está en uso. Prueba con otro.'


def login_vista(request):
    if request.user.is_authenticated:
        return redirect('inicio:inicio')

    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        password = request.POST.get('password', '')
        usuario = authenticate(request, username=correo, password=password)

        if usuario is None:
            messages.error(request, 'Error. Revisa tu correo y tu contraseña.')
        else:
            login(request, usuario)
            siguiente = request.POST.get('next', '')
            # Solo se redirige a direcciones de este mismo sitio
            if siguiente and url_has_allowed_host_and_scheme(
                siguiente,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(siguiente)
            return redirect('inicio:inicio')

    return render(request, 'cuentas/inicio_sesion.html')


@require_POST
def logout_vista(request):
    logout(request)
    return redirect('inicio:inicio')


def registro_vista(request):
    if request.user.is_authenticated:
        return redirect('inicio:inicio')

    errores = {}
    valores = {}

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        valores = {campo: request.POST.get(campo, '') for campo in CAMPOS_USUARIO}

        if form.is_valid():
            datos = form.cleaned_data
            try:
                with transaction.atomic():
                    User.objects.create_user(
                        username=datos['username'],
                        email=datos['correo'],
                        password=datos['contrasena'],
                        first_name=datos['nombre'],
                        last_name=datos['apellidos'],
                        fecha_de_nacimiento=datos.get('fecha_nacimiento'),
                        ciudad=datos['ciudad'],
                    )
            except IntegrityError:
                errores = {'username': USUARIO_REPETIDO}
            else:
                messages.success(request, 'Listo. Tu cuenta quedó creada. Inicia sesión para continuar.')
                return redirect('cuentas:login')
        else:
            errores = errores_a_dict(form)

    return render(request, 'cuentas/crear_cuenta.html', {
        'errores': errores,
        'valores': valores,
    })


@login_required
def registro_promotor_vista(request):
    if hasattr(request.user, 'promotor'):
        return redirect('crear_evento:crear_evento')

    errores = {}
    valores = {}

    if request.method == 'POST':
        form = RegistroPromotorForm(request.POST)
        valores = {campo: request.POST.get(campo, '') for campo in ('organizacion', 'telefono')}

        if form.is_valid():
            datos = form.cleaned_data
            try:
                with transaction.atomic():
                    Promotor.objects.create(
                        usuario=request.user,
                        organizacion=datos['organizacion'],
                        telefono=datos['telefono'],
                    )
            except IntegrityError:
                messages.error(request, 'Ocurrió un error al registrarte como promotor.')
            else:
                messages.success(request, '¡Listo! Tu cuenta de promotor ha quedado registrada.')
                return redirect('inicio:inicio')
        else:
            errores = errores_a_dict(form)

    return render(request, 'cuentas/crear_cuenta_promotor.html', {
        'errores': errores,
        'valores': valores,
    })