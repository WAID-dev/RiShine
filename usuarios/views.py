from django.contrib.auth import logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Usuario


# Create your views here.
@login_required
def perfil(request):
    """
        Permite al usuario autenticado visualizar y actualizar
        la información básica de su perfil.
    """

    if request.method == "POST":
        # Obtiene y limpia los datos enviados desde el formulario
        username = request.POST.get('nombreUsuario', '').strip()
        nombre =request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        correo = request.POST.get('correo', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()
        fecha_de_nacimiento = request.POST.get('fecha_de_nacimiento', '').strip()

        if not correo or not username:
            messages.error(request, 'El nombre de usuario y el correo son obligatorios.')
            return redirect('usuarios:perfil')

        if correo:
            try:
                validate_email(correo)
            except ValidationError:
                messages.error(request, 'El correo no tiene un formato valido.')
                return redirect('usuarios:perfil')

        if Usuario.objects.filter(email=correo).exclude(pk=request.user.pk).exists():
            messages.error(request, 'El correo ya esta registrado.')
            return redirect('usuarios:perfil')

        if Usuario.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            messages.error(request, 'El username ya esta registrado.')
            return redirect('usuarios:perfil')

        # Actualiza la información del usuario autenticado
        request.user.username = username
        request.user.first_name = nombre
        request.user.last_name = apellido
        request.user.email = correo
        request.user.ciudad = ciudad
        request.user.fecha_de_nacimiento = fecha_de_nacimiento or None
        request.user.save(update_fields=['username','first_name', 'last_name', 'email', 'ciudad', 'fecha_de_nacimiento'])

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('usuarios:perfil')

    return render(request, 'usuarios/perfil.html', {
        'usuario': request.user
    })

@login_required
def eliminar_cuenta(request):
    """
        Permite eliminar la cuenta del usuario autenticado
        junto con la información relacionada
    """
    if request.method == "POST":
        user = request.user

        # Cierra la sesión antes de eliminar la cuenta
        logout(request)

        # Si es promotor, borra primero
        # los eventos asociados para evitar errores
        # de integridad referencial
        if hasattr(user, 'promotor'):
            user.promotor.evento_promotor.all().delete()
            user.promotor.delete()

        # Elimina la cuenta de usuario
        user.delete()

        messages.success(request, 'Tu cuenta ha sido eliminada.')
        return redirect('/')
    return redirect('usuarios:perfil')



@require_POST
def cerrar_sesion(request):
    # Cierra la sesion del usario actual y lo manda al inicio
    logout(request)
    return redirect('/')




