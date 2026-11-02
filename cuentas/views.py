from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import RegistroPromotorForm, RegistroUsuarioForm, errores_a_dict
from .models import Perfil, Promotor

User = get_user_model()

# Campos que se devuelven a la plantilla para no perderlos si hay un error.
# Las contraseñas nunca se devuelven.
CAMPOS_USUARIO = ('nombre', 'apellidos', 'username', 'correo', 'fecha_nacimiento')
CAMPOS_PROMOTOR = ('nombre', 'apellidos', 'username', 'correo', 'organizacion')

USUARIO_REPETIDO = 'Ese nombre de usuario ya está en uso. Prueba con otro.'


def login_vista(request):
    if request.user.is_authenticated:
        return redirect('inicio:inicio')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        usuario = authenticate(request, username=username, password=password)

        if usuario is None:
            messages.error(request, 'Error. Revisa tu nombre de usuario y tu contraseña.')
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
                    usuario = User.objects.create_user(
                        username=datos['username'],
                        email=datos['correo'],
                        password=datos['contrasena'],
                        first_name=datos['nombre'],
                        last_name=datos['apellidos'],
                    )
                    Perfil.objects.create(
                        usuario=usuario,
                        fecha_nacimiento=datos['fecha_nacimiento'],
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


def registro_promotor_vista(request):
    if request.user.is_authenticated:
        return redirect('inicio:inicio')

    errores = {}
    valores = {}

    if request.method == 'POST':
        form = RegistroPromotorForm(request.POST, request.FILES)
        valores = {campo: request.POST.get(campo, '') for campo in CAMPOS_PROMOTOR}

        if form.is_valid():
            datos = form.cleaned_data
            try:
                with transaction.atomic():
                    usuario = User.objects.create_user(
                        username=datos['username'],
                        email=datos['correo'],
                        password=datos['contrasena'],
                        first_name=datos['nombre'],
                        last_name=datos['apellidos'],
                    )
                    Perfil.objects.create(usuario=usuario)
                    Promotor.objects.create(
                        usuario=usuario,
                        organizacion=datos['organizacion'],
                        ine=datos['ine'],
                    )
            except IntegrityError:
                errores = {'username': USUARIO_REPETIDO}
            else:
                messages.success(request, 'Listo. Tu cuenta de promotor quedó creada. Inicia sesión para continuar.')
                return redirect('cuentas:login')
        else:
            errores = errores_a_dict(form)

    return render(request, 'cuentas/crear_cuenta_promotor.html', {
        'errores': errores,
        'valores': valores,
    })