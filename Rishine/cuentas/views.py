from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme

from usuarios.models import Promotor


def crear_cuenta(request):
    return render(request, 'cuentas/crear_cuenta.html')


def inicio_sesion(request):
    if request.method == 'GET':
        next_url = request.GET.get('next') or '/'
        return redirect(f'/?show_login=1&next={next_url}')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        next_url = request.POST.get('next') or request.GET.get('next') or '/'

        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next_url = '/'

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)

        messages.error(request, 'Usuario o contraseña invalidos.')
        return redirect(f'/?show_login=1&next={next_url}')

    return render(request, 'cuentas/inicio_sesion.html')


@login_required(login_url='/?show_login=1')
def crear_cuenta_promotor(request):
    next_url = request.POST.get('next') or request.GET.get('next') or '/'

    if hasattr(request.user, 'promotor'):
        return redirect(next_url)

    if request.method == 'POST':
        organizacion = request.POST.get('organizacion', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        if organizacion and telefono:
            Promotor.objects.create(usuario=request.user, organizacion=organizacion, telefono=telefono)
            messages.success(request, 'Cuenta de promotor creada correctamente.')
            return redirect(next_url)
        messages.error(request, 'Organizacion y telefono son obligatorios.')

    return render(request, 'cuentas/crear_cuenta_promotor.html')
