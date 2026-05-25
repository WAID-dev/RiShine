from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.models import User

from usuarios.models import Promotor


def crear_cuenta(request):
    """
    Permite registrar nuevas cuentas de usuario
    dentro de la plataforma.
    """
    if request.method == 'POST':
        # Obtiene y limpia los datos enviados
        # desde el formulario de registro
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        # Verifica que todos los campos obligatorios contengan información
        if not all([first_name, last_name, username, email, password1, password2]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'cuentas/crear_cuenta.html')

        # Verifica que ambas contraseñas coincidan
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'cuentas/crear_cuenta.html')

        # Evita registrar nombres de usuario duplicados
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya esta en uso.')
            return render(request, 'cuentas/crear_cuenta.html')

        # Crea el nuevo usuario utilizando
        # el sistema de autenticación de Django
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )
        user.save()

        messages.success(request, 'Cuenta creada exitosamente. Inicia sesión.')
        return redirect('cuentas:login')

    return render(request, 'cuentas/crear_cuenta.html')

def inicio_sesion(request):
    """
    Permite autenticar usuarios y crear
    una sesión activa dentro de la plataforma
    """

    # Redirige al formulario de inicio de sesión
    # mostrado desde la página principal
    if request.method == 'GET':
        next_url = request.GET.get('next') or '/'
        return redirect(f'/?show_login=1&next={next_url}')

    if request.method == 'POST':
        # Obtiene las credenciales ingresadas por el usuario
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        next_url = request.POST.get('next') or request.GET.get('next') or '/'

        # Verifica que la URL de redirección
        # pertenezca al mismo dominio para evitar
        # redirecciones inseguras
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next_url = '/'

        # Autentica las credenciales del usuario
        user = authenticate(request, username=username, password=password)

        # Si las credenciales son válidas,
        # inicia sesión y redirige
        if user is not None:
            login(request, user)
            return redirect(next_url)

        messages.error(request, 'Usuario o contraseña invalidos.')
        return redirect(f'/?show_login=1&next={next_url}')

    return render(request, 'cuentas/inicio_sesion.html')


@login_required(login_url='/?show_login=1')
def crear_cuenta_promotor(request):
    """
    Permite convertir un usuario autenticado
    en promotor para habilitar la publicación
    de eventos
    """
    next_url = request.POST.get('next') or request.GET.get('next') or '/'

    # Evita crear múltiples cuentas de promotor para el mismo usuario
    if hasattr(request.user, 'promotor'):
        return redirect(next_url)

    if request.method == 'POST':
        # Obtiene los datos requeridos para el registro del promotor
        organizacion = request.POST.get('organizacion', '').strip()
        telefono = request.POST.get('telefono', '').strip()

        # Verifica que los campos obligatorios contengan información
        if organizacion and telefono:
            # Crea el perfil de promotor asociado al usuario autenticado
            Promotor.objects.create(usuario=request.user, organizacion=organizacion, telefono=telefono)
            messages.success(request, 'Cuenta de promotor creada correctamente.')
            return redirect(next_url)
        messages.error(request, 'Organizacion y telefono son obligatorios.')

    return render(request, 'cuentas/crear_cuenta_promotor.html')
